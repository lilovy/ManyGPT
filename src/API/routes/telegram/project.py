from fastapi import APIRouter, Depends, Request, status

from ...models.project import UserProject, NewUserProject
# from ....database.db import DBHelper


router = APIRouter(prefix="/project", tags=["project"])


@router.get("/all")
def get_user_projects(
    user_id: int,
    db: DBHelper = Depends(get_db),
    ):
    user = db.get_user()

    user_id = request.state.user.get("user_id")
    projects = db.get_user_projects(user_id)

    return projects


@router.get("/")
def get_user_project(
    project: UserProject,
    db: DBHelper = Depends(get_db),
    ):
    db.get_user_data_files(
        project.project_id,
    )
    return {"status": status.HTTP_200_OK}


@router.post("/new")
def add_user_project(
    project: NewUserProject,
    db: DBHelper = Depends(get_db),
    ):

    db.add_project(
        user_id=project.user_id,
        name=project.name,
        mimetype=project.mimetype,
        model_id=project.model_id,
        prompt=project.prompt,
        file=project.file,
    )
    
    return {"status": status.HTTP_201_CREATED}

