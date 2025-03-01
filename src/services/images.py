import shutil

from fastapi import BackgroundTasks, UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImagesService(BaseService):
    def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks):
        image_path = f"src/static/images/{file.filename}"
        with open(f"src/static/images/{file.filename}", "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        background_tasks.add_task(resize_image, image_path)
