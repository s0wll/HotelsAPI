import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображения"])

@router.post("")  # Ручка с таской Celery
def upload_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(f"src/static/images/{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(image_path)

# @router.post("")  # Ручка с таской без Celery, напрямую через FastAPI
# def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
#     image_path = f"src/static/images/{file.filename}"
#     with open(f"src/static/images/{file.filename}", "wb+") as new_file:
#         shutil.copyfileobj(file.file, new_file)

#     background_tasks.add_task(resize_image, image_path)