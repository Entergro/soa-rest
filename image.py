import os

from fastapi import UploadFile, File, APIRouter, HTTPException

import schemas

router = APIRouter()


@router.post("/image/{user_name}", response_model=schemas.ImageUrl)
async def create_image(name: str, file: UploadFile = File(...)):
    picture = open(f"images/{name}.png", "wb")
    picture.write(await file.read())
    return {"imageUrl": f"http://127.0.0.1:8000/images/{name}.png"}


@router.delete("/image/{user_name}")
async def delete_image(name: str):
    if not os.path.exists(f"images/{name}.png"):
        raise HTTPException(status_code=404, detail="Image not found")
    os.remove(f"images/{name}.png")
    return 'OK'


@router.post("/image/update/{user_name}", response_model=schemas.ImageUrl)
async def edit_image(name: str, file: UploadFile = File(...)):
    if not os.path.exists(f"images/{name}.png"):
        raise HTTPException(status_code=404, detail="Image not found")
    os.remove(f"images/{name}.png")
    picture = open(f"images/{name}.png", "wb")
    picture.write(await file.read())
    return {"imageUrl": f"http://127.0.0.1:8000/images/{name}.png"}
