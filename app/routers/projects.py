from typing import Optional
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
import time

from app.controllers import projects
from app.controllers.cameras import cameras
from app.models.project import Project

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Project])
async def get_projects():
    return projects.get_projects()


@router.get("/{project_name}", response_model=Project)
async def get_project(project_name: str):
    return projects.get_project(project_name)


@router.delete("/{project_name}", response_model=bool)
async def delete_project(project_name: str):
    return projects.delete_project(projects.get_project(project_name))


@router.post("/{project_name}", response_model=Project)
async def new_project(project_name: str):
    return projects.new_project(project_name)


@router.put("/{project_name}/photo", response_model=bool)
async def add_photo(project_name: str, camera_id: int):
    camera = cameras.get_camera(camera_id)
    camera_controller = cameras.get_camera_controller(camera)
    photo = camera_controller.photo(camera)
    projects.add_photo(projects.get_project(project_name), photo)

    return True


@router.put("/{project_name}/photo_stack", response_model=bool)
async def add_photo_stack(project_name: str, camera_id: int, focus_min: int, focus_max: int):
    camera = cameras.get_camera(camera_id)
    camera_controller = cameras.get_camera_controller(camera)
    project = projects.get_project(project_name)
    stack_number = projects.get_number_stacks(project)

    # needs one focusing before stack, todo: debug
    camera_controller.set_focus(camera, False, focus_min)
    time.sleep(2.5) # give time to focus, todo: blocking call available?

    for i,f in enumerate(range(focus_min, focus_max+1)):
        camera_controller.set_focus(camera, False, f)
        time.sleep(0.5) # give time to focus
        photo = camera_controller.photo(camera)
        projects.add_stack_photo(project, photo, stack_number, i)

    return True