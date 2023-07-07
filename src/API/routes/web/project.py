from fastapi import APIRouter, Depends, Request, status, Query

from ....core.llms import LLMs
from ...models.project import UserProject, NewUserProject
from ...dependencies.dependencies import *
from ....database.db import DBHelper


router = APIRouter(prefix="/project", tags=["project"])


@router.get("/count")
async def get_count_projects(
    request: Request,
    db: DBHelper = Depends(get_db),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")
    count = db.get_project_count(
        user_id,
    )
    return {
        "user_id": user_id,
        "projects": count,
    }


@router.get("/all")
async def get_user_projects(
    request: Request,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")
    projects = db.get_user_projects(user_id, offset, limit)

    project = {"user_id": 123, "name": "pj2", "file": "cats.png"}

    return projects


@router.get("/file")
async def get_user_project_file(
    request: Request,
    project: UserProject,
    db: DBHelper = Depends(get_db),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != model.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

    content = db.get_user_data_files(
        project.project_id,
    )
    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename={project.name}.txt"
        }
    )


@router.post("/new")
async def add_user_project(
    request: Request,
    project: NewUserProject,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != project.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

    llm.new_bot(
        project.name,
        project.prompt,
        project.model,
    )

    db.add_project(
        user_id=project.user_id,
        name=project.name,
        mimetype=project.mimetype,
        model_id=project.model_id,
        prompt=project.prompt,
        file=project.file,
    )
    
    return {"status": status.HTTP_201_CREATED}