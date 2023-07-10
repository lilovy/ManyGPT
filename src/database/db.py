import datetime
import os.path
from sqlalchemy import and_
import sqlalchemy
from src.database.model.enums import *
from sqlalchemy.orm import sessionmaker
from src.database.model.database_elems import Base, UserToken, User, UserLLM, ProjectLLM, \
    Project, FilePart, ResultData, SubscriptionType, Conversation, Message, LLM, CurrConvo


class DBHelper:
    __engine = None

    def __init__(self, db_path):
        self.__db_path = db_path
        self.__engine = sqlalchemy.create_engine(f'{db_path}', echo=True)
        # self.create_db()

    def create_db(self):
        # if not os.path.exists(f"{self.__db_path}"):
        Base.create_db(self.__engine)
        with self.__create_session() as session:
            free_type = SubscriptionType(name=SubscriptionLevelEnum.free, limit=30)
            basic_type = SubscriptionType(name=SubscriptionLevelEnum.basic, limit=1000000)
            advanced_type = SubscriptionType(name=SubscriptionLevelEnum.advanced, limit=10000000)
            gpt = LLM(ModelEnum.ChatGPT)
            claude = LLM(ModelEnum.Claude)
            session.add_all([free_type, basic_type, advanced_type, gpt, claude])
            session.commit()

    def __create_session(self):
        Session = sessionmaker(bind=self.__engine)
        return Session()

    def get_user(self, user_id: int) -> dict:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            user_info = user.get_simple_dict()
            user_info["subscription"] = user.subscription_type.get_simple_dict()
            user_info["token"] = user.user_token[0].get_simple_dict()

            all_llms = user.user_llm
            if all_llms is None or all_llms.__len__() == 0:
                user_info["default_model"] = None
            else:
                for llm in all_llms:
                    if llm.is_default:
                        default_llm = llm
                        break
                if default_llm is None:
                    user_info["default_model"] = None
                else:
                    user_info["default_model"] = default_llm.get_simple_dict()
        return user_info

    def get_user_conversations(self, user_id: int, offset: int, limit: int) -> list[dict]:
        conversations = []
        with self.__create_session() as session:
            conversations_list = session.query(Conversation).filter(Conversation.user_id == user_id).offset(offset).limit(limit).all()
            for c in conversations_list:
                conversation_info = c.get_simple_dict()
                conversation_info["user_id"] = c.user_id
                user_llm = c.user_llm
                conversation_info["llm"] = user_llm.get_simple_dict()
                conversation_info["llm"]["system_name"] = user_llm.system_name
                conversations.append(conversation_info)
        return conversations

    def get_user_models(self, user_id: int, offset: int, limit: int) -> list[dict]:
        models_info = []
        try:
            with self.__create_session() as session:
                user_llms = session.query(UserLLM).filter(UserLLM.user_id == user_id).offset(offset).limit(limit).all()
                for model in user_llms:
                    model_info = model.get_full_dict()
                    model_info["model"] = model.llm.get_simple_dict()
                    models_info.append(model_info)
            return models_info
        except sqlalchemy.orm.exc.NoResultFound:
            return []
        finally:
            return models_info

    def get_user_projects(self, user_id: int, offset: int, limit: int) -> list[dict]:
        projects = []
        try:
            with self.__create_session() as session:
                projects_list = session.query(Project).filter(Project.user_id == user_id).offset(offset).limit(limit).all()
                for p in projects_list:
                    project_info = p.get_simple_dict()
                    if p.project_llm is None:
                        continue
                    project_info["model"] = p.project_llm.get_simple_dict()
                    project_info["model"]["system_name"] = p.name
                    projects.append(project_info)
            return projects
        except sqlalchemy.orm.exc.NoResultFound:
            return []
        finally:
            return projects

    def get_user_data_files(self, project_id: int) -> list:
        datas = []
        with self.__create_session() as session:
            datas_list = session.query(ResultData).filter(ResultData.project_id == project_id).all()
        for rd in datas_list:
            datas.append(rd.data)
        return datas

    def get_user_msg_history(self, conversation_id: int, offset: int, limit: int) -> list[dict]:
        messages_info = []
        try:
            with self.__create_session() as session:
                messages = session.query(Message).filter(Message.conversation_id == conversation_id)\
                    .offset(offset).limit(limit).all()
                for message in messages:
                    message_info = message.get_simple_dict()
                    message_info["conversation"] = message.conversation.get_simple_dict()
                    messages_info.append(message_info)
        except sqlalchemy.orm.exc.NoResultFound:
            return []
        finally:
            return messages_info

    def get_project_count(self, user_id: int) -> int:
        result: int
        with self.__create_session() as session:
            projects_list = session.query(Project).filter(Project.user_id == user_id).all()
            result = projects_list.__len__()
        return result

    def get_message_count(self, convo_id: int) -> int:
        result: int
        with self.__create_session() as session:
            messages = session.query(Message).filter(Message.conversation_id == convo_id).all()
            result = messages.__len__()
        return result

    def get_model_count(self, user_id: int) -> int:
        result: int
        with self.__create_session() as session:
            user_llm_list = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()
            result = user_llm_list.__len__()
        return result

    def get_count_conversation(self, user_id: int) -> int:
        result: int
        with self.__create_session() as session:
            conversations = session.query(Conversation).filter(Conversation.user_id == user_id).all()
            result = conversations.__len__()
        return result

    def get_base_model(self, model_id: int = None):
        with self.__create_session() as session:
            if model_id is None:
                llm_list = []
                llms = session.query(LLM).all()
                for llm in llms:
                    llm_list.append(llm.get_simple_dict())
                return llm_list
            else:
                llm = session.query(LLM).filter(LLM.id == model_id).first()
                if llm is not None:
                    return llm.model.value
                else:
                    return None

    def add_user(self, user_id: int, username: str) -> None:
        limit: int
        with self.__create_session() as session:
            test_user = session.get(User, user_id)
            if test_user is not None:
                return
            free_subscription = session.query(SubscriptionType)\
                .filter(SubscriptionType.name == SubscriptionLevelEnum.free).first()

            user = User(user_id=user_id, username=username, subscription_type_id=free_subscription.id)
            session.add(user)
            limit = free_subscription.limit
            session.commit()
        self.__init_user_token(user_id=user_id, limit=limit)
        self.__init_curr_convo(user_id)

    def __init_user_token(self, user_id: int, limit: int) -> None:
        user_token = UserToken(user_id=user_id, count=limit)
        with self.__create_session() as session:
            session.add(user_token)
            session.commit()

    def __init_curr_convo(self, user_id: int):
        currconvo = CurrConvo(user_id)
        with self.__create_session() as session:
            session.add(currconvo)
            session.commit()

    def add_user_model(self, user_id: int, name: str, system_name: str, base_model_id: int, prompt: str):
        with self.__create_session() as session:
            all_models_this_user = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()

            model = UserLLM(user_id=user_id, name=name, system_name=system_name, base_model_id=base_model_id,
                            prompt=prompt, is_default=all_models_this_user.__len__() == 0)

            session.add(model)
            session.commit()

    def add_chat(self, user_id: int, name: str, user_model_id: int) -> None:
        chat = Conversation(user_id=user_id, name=name, llm_id=user_model_id)
        new_chat_id: int
        with self.__create_session() as session:
            session.add(chat)
            session.commit()
            new_chat_id = chat.id
        self.__change_curr_convo(user_id, new_chat_id)

    def __change_curr_convo(self, user_id: int, convo_id : int):
        with self.__create_session() as session:
            currconvo = session.query(CurrConvo).filter(CurrConvo.user_id == user_id).first()
            currconvo.convo_id = convo_id
            session.commit()

    def add_message(self, convo_id: int, question: str, answer: str) -> None:
        message = Message(conversation_id=convo_id, question=question, answer=answer)
        user_id: int
        with self.__create_session() as session:
            session.add(message)
            conversation = session.get(Conversation, convo_id)
            user_id = conversation.user.id
            session.commit()
        self.__user_asked(user_id)

    def add_project(self, user_id: int, name: str, system_name: str, model_id: int, mimetype: str, file: bytes, prompt: str) -> None:
        project_llm_id = self.__create_project_llm_and_get_new_id(system_name=system_name,llm_id=model_id, prompt=prompt)
        project = Project(user_id=user_id, name=name, model_id=project_llm_id, mimetype=mimetype, file=file)
        with self.__create_session() as session:
            session.add(project)
            session.commit()
            self.__add_file_parts(project_id=project.id, full_text=str(file, "utf-8"))

    def __create_project_llm_and_get_new_id(self, system_name: str, llm_id: int, prompt: str):
        project_llm = ProjectLLM(model_id=llm_id, system_name=system_name, prompt=prompt)
        with self.__create_session() as session:
            session.add(project_llm)
            session.commit()
            return project_llm.id

    def __add_file_parts(self, project_id: int, full_text: str):
        rows = full_text.split('\n')
        full_file = []
        with self.__create_session() as session:
            for r in rows:
                full_file.append(FilePart(r, project_id))
            session.add_all(full_file)
            session.commit()

    def add_result_data(self, project_id: int, data: str) -> None:
        result_data = ResultData(project_id=project_id, data=data)
        with self.__create_session() as session:
            session.add(result_data)
            session.commit()

    def update_default_model(self, user_id: int, new_default_model_id: int) -> None:
        with self.__create_session() as session:
            user_llms = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()
            # Check what that user has user_llm with id = user_model_id
            if user_llms is not None and any(model.id == new_default_model_id for model in user_llms):
                for model in user_llms:
                    model.is_default = False
                    if model.id == new_default_model_id:
                        model.is_default = True
                session.commit()

    def update_plan(self, user_id: int, plan: str) -> None:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            subscription = session.query(SubscriptionType).filter(SubscriptionType.name == plan).first()
            if user is not None and subscription is not None:
                user.subscription_id = subscription.id
                session.commit()

    def update_limits(self,  new_limit: int) -> None:
        with self.__create_session() as session:
            subscription = session.query(SubscriptionType).filter(SubscriptionType.name == "free").first()
            if subscription is not None:
                subscription.limit = new_limit
                session.commit()

    def can_user_ask_question(self, user_id: int) -> bool:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            user_token = user.user_token[0]
            if user_token.last_update.date() < datetime.date.today():
                subscription = user.subscription_type
                user_token.count = subscription.limit
                session.commit()
                return True
            else:
                return user_token.count > 0

    def __user_asked(self, user_id: int) -> None:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            user_token = user.user_token[0]
            user_token.count -= 1
            user_token.last_update = datetime.date.today()
            session.commit()

    def get_user_count_for_statistic(self) -> dict[str, int]:
        count_free, count_basic, count_advanced, count_all = 0, 0, 0, 0
        with self.__create_session() as session:
            users = session.query(User).all()
            for some_user in users:
                count_all += 1
                match some_user.subscription_type.name:
                    case SubscriptionLevelEnum.free:
                        count_free += 1
                    case SubscriptionLevelEnum.basic:
                        count_basic += 1
                    case SubscriptionLevelEnum.advanced:
                        count_advanced += 1
        return {
            "free": count_free,
            "basic": count_basic,
            "advanced": count_advanced,
            "all": count_all
        }

    def get_interactive_count(self, date_start: datetime.datetime, date_end: datetime.datetime) -> int:
        result: int
        with self.__create_session() as session:
            messages = session.query(Message).filter(and_(date_start <= Message.time, Message.time <= date_end)).all()
            if messages is not None:
                result = messages.__len__()
            else:
                result = 0
        return result

    def get_new_user_count(self, date_start: datetime.datetime, date_end: datetime.datetime) -> int:
        result: int
        with self.__create_session() as session:
            users = session.query(User).filter(and_(date_start <= User.registration_date, User.registration_date <= date_end)).all()
            if users is not None:
                result = users.__len__()
            else:
                result = 0
        return result

    def get_user_subscribe_level(self, user_id: int) -> str | None:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            if user is not None:
                return user.subscription_type.name.value
        return None

    def user_growth(self, plan: str = None, period: int = 7) -> dict:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=period)
        result = {}
        with self.__create_session() as session:
            users_data = []
            users = session.query(User).filter(
                and_(start_date <= User.registration_date, User.registration_date <= end_date)).all()
            if users is None:
                return {}
            if plan is not None:
                for user in users:
                    if user.subscription_type.name.value == plan:
                        users_data.append(user)
            else:
                users_data = users
            for day in range(period):
                some_date = end_date.date() - datetime.timedelta(day)
                count = 0
                for user in users_data:
                    if user.registration_date.date() == some_date:
                        count += 1
                result[some_date] = count

        return result

    def amount_of_interaction(self, period: int = 7):
        result = {}
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=period)
        with self.__create_session() as session:
            messages = session.query(Message).filter(and_(start_date <= Message.time, Message.time <= end_date)).all()
            if messages is None:
                return {}
            for day in range(period):
                some_date = end_date.date() - datetime.timedelta(day)
                count = 0
                for message in messages:
                    if message.time.date() == some_date:
                        count += 1
                result[some_date] = count
        return result

    def get_project_name(self, project_id: int) -> str:
        with self.__create_session() as session:
            project = session.get(Project, project_id)
            return project.name

    def get_conversation_model(self, convo_id: int) -> str | None:
        with self.__create_session() as session:
            conv = session.get(Conversation, convo_id)
            if conv is None:
                return None
            elif conv.user_llm is None:
                return None
            else:
                return conv.user_llm.system_name

    def get_curr_convo_id(self, user_id: int) -> int | None:
        with self.__create_session() as session:
            currconvo = session.query(CurrConvo).filter(CurrConvo.user_id == user_id).first()
            if currconvo is None:
                return None
            else:
                return currconvo.convo_id

    def get_subs(self) -> list[dict]:
        result = []
        with self.__create_session() as session:
            subscriptions = session.query(SubscriptionType).all()
            for sub in subscriptions:
                result.append(sub.get_simple_dict())
        return result

    def get_raw_files(self, project_id: int) -> list:
        result = []
        with self.__create_session() as session:
            fileParts = session.query(FilePart).filter(FilePart.project_id == project_id).all()
            if fileParts is not None:
                for f in fileParts:
                    result.append(f.part)
        return fileParts
