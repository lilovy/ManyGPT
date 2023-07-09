from fastapi import APIRouter, Depends, Request, status, Query, Response, UploadFile
from fastapi.responses import FileResponse
from typing import List

from ....core.llms import LLMs
from ...models.project import UserProject, NewUserProject, Projects
from ...models.subscription import Subs
from ...models.responses import ResponseStatus
from ...models.count import Count
from ...dependencies.dependencies import *
from ....database.db import DBHelper


router = APIRouter(prefix="/project", tags=["project"])


@router.get("/count", response_model=Count, status_code=200)
async def get_count_projects(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_project_count(user_id)
    return Count(
        user_id=user_id,
        object="projects",
        count=count,
    )


@router.get("/all", response_model=List[Projects], status_code=200)
async def get_user_projects(
    user_id: int,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
    ):

    projects = db.get_user_projects(user_id, offset, limit)

    # return [Projects(**project) for project in projects]
    return projects


@router.get("/file", response_class=FileResponse)
async def get_user_project(
    project_id: int,
    name: str,
    db: DBHelper = Depends(get_db),
    ):
    content = db.get_user_data_files(
        project_id,
    )
    content = "\n".join(content)

    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename={name}.txt"
        }
    )


@router.get("/access", responses={200: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
def сhecking_project_access(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    if db.get_user_subscribe_level(user_id) == Subs.advanced.value:
        return {"status": status.HTTP_200_OK}

    return {"status": status.HTTP_401_UNAUTHORIZED}


@router.post("/new", responses={201: {"model": ResponseStatus}})
async def add_user_project(
    # project: NewUserProject,
    user_id: int,
    name: str,
    system_name: str,
    model_id: int,
    prompt: str,
    file: UploadFile,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
    ):

    base_model = db.get_base_model(model_id)

    llm.new_bot(
        name,
        prompt,
        base_model,
    )

    db.add_project(
        user_id=user_id,
        name=name,
        mimetype=file.content_type,
        model_id=model_id,
        prompt=prompt,
        system_name=system_name,
        file=await file.read(),
    )

    return {"status": status.HTTP_201_CREATED}

