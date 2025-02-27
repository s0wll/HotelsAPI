from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.services.images import ImagesService


router = APIRouter(prefix="/images", tags=["Изображения"])


# @router.post("")  # Ручка с таской Celery
# def upload_image(file: UploadFile):
#     image_path = f"src/static/images/{file.filename}"
#     with open(f"src/static/images/{file.filename}", "wb+") as new_file:
#         shutil.copyfileobj(file.file, new_file)

#     resize_image.delay(image_path)


@router.post("")  # Ручка с таской без Celery, напрямую через FastAPI
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)
    return {"status": "OK"}
