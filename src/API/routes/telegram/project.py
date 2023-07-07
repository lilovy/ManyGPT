from fastapi import APIRouter, Depends, Request, status

from ...models.project import UserProject, NewUserProject
from ...dependencies.dependencies import *
from ....database.db import DBHelper


router = APIRouter(prefix="/project", tags=["project"])


@router.get("/count")
async def get_count_projects(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_project_count(user_id)
    return {
        "user_id": user_id,
        "projects": count,
    }


@router.get("/all")
async def get_user_projects(
    user_id: int,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
    ):

    projects = db.get_user_projects(user_id, offset, limit)

    return projects


@router.get("/")
async def get_user_project(
    project: UserProject,
    db: DBHelper = Depends(get_db),
    ):
    content = db.get_user_data_files(
        project.project_id,
    )
    return content


@router.post("/new")
async def add_user_project(
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

