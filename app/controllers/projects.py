from datetime import datetime
import io
import pathlib
from tempfile import TemporaryFile
from typing import IO
import uuid
from zipfile import ZipFile
import orjson
import os
import shutil
import time

from app.controllers.cameras import cameras
from app.models.camera import Camera

from app.models.project import Project
from app.config import config

ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png")

def get_projects() -> list[Project]:
    return [
        get_project(folder)
        for folder in os.listdir(config.projects_path)
        if os.path.exists(
            config.projects_path.joinpath(folder, "openscan_project.json")
        )
    ]

def _get_project_path(project_name: str) -> pathlib.Path:
    return config.projects_path.joinpath(project_name)

def _get_project_photos(project_path: pathlib.Path) -> list[str]:
    photos = [file for file in os.listdir(project_path) if file.lower().endswith(ALLOWED_EXTENSIONS)]
    return photos

def get_project(project_name: str) -> Project:
    project_path = _get_project_path(project_name)
    photos = _get_project_photos(project_path)
    with open(project_path.joinpath("openscan_project.json")) as f:
        return Project(name=project_name, path=project_path, photos=photos, **orjson.loads(f.read()))

def get_number_stacks(project: Project) -> int:
    photos = _get_project_photos(project.path)

    # if picture names end with -0,-1,... then we have a focus stack -> counts as only one
    photos = [p.rsplit('.')[0] for p in photos] # remove extension
    photos = [''.join(p.rsplit('-')[:-1]) if '-' in p else p for p in photos] # remove trailing number for focus step
    num_unique = len(set(photos)) # find unique names

    return num_unique

def delete_project(project: Project) -> bool:
    shutil.rmtree(project.path)
    return True

def save_project(project: Project):
    os.makedirs(project.path, exist_ok=True)
    with open(project.path.joinpath("openscan_project.json"), "wb") as f:
        f.write(orjson.dumps({"created": project.created, "uploaded": project.uploaded}))

def new_project(project_name: str) -> Project:
    projects = get_projects()
    if project_name in [project.name for project in projects]:
        raise ValueError(f"Project {project_name} already exists")
    project_path = _get_project_path(project_name)
    project = Project(name=project_name, path=project_path, created=datetime.now())
    save_project(project)
    return project


def add_photo(project: Project, photo: io.BytesIO) -> bool:
    with open(
        project.path.joinpath(f"photo_{len(project.photos):>04}.jpg"), "wb"
    ) as f:
        f.write(photo.read())
        project.photos.append(f.name)
    return True

def add_stack_photo(project: Project, photo: io.BytesIO, picture_num: int, focus_num: int) -> bool:
    with open(
        project.path.joinpath(f"photo_0_{picture_num+1}-{focus_num}.jpg"), "wb"
    ) as f:
        f.write(photo.read())
        project.photos.append(f.name)
    return True

def compress_project_photos(project: Project) -> IO[bytes]:
    file = TemporaryFile()
    with ZipFile(file, "w") as zipf:
        counter = 1
        for photo in project.photos:
            zipf.write(project.path.joinpath(photo), photo)
            print(f"{photo} - {counter}/{len(project.photos)}")
            counter += 1
    return file


def split_file(file: IO[bytes]) -> list[io.BytesIO]:
    file.seek(0, 2)
    file.seek(0)

    chunk = file.read(config.cloud.split_size)
    while chunk:
        yield io.BytesIO(chunk)
        chunk = file.read(config.cloud.split_size)
