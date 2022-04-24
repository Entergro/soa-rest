import pickle
import time
from typing import List

import pika
from fastapi import Depends, HTTPException

import crud
import schemas
from db import get_db
from sqlalchemy.orm import Session

from fastapi import APIRouter

from db import channel

router = APIRouter()


@router.get("/users/", response_model=List[schemas.UserBase])
async def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@router.get("/users/{name}", response_model=schemas.UserBase)
async def get_user(name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(name, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/", response_model=schemas.UserBase)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(name=user.name, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(user=user, db=db)


@router.delete("/users/")
def delete_user(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(name=name, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db_user, db)


@router.post("/users/update",response_model=schemas.UserBase)
def edit_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(name=user.name, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.edit_user(user=user, db=db)


@router.post("/users/statictics/{name}")
def get_statistics(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(name=name, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    fileid = str(time.time())
    message = {'name': name, 'fileid': fileid}
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=pickle.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    return {"imageUrl": f"http://127.0.0.1:8000/pdf/{name}_{fileid}.pdf"}

@router.post("/users/statictics/win/{name}")
def add_win(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(name=name, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.wins += 1
    db_user.count_of_session += 1
    db.commit()
    return 'OK'


@router.post("/users/statictics/fail/{name}")
def add_fail(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(name=name, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.fails += 1
    db_user.count_of_session += 1
    db.commit()
    return 'OK'


@router.post("/users/statictics/sec/{name}")
def add_sec(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(name=name, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.secs += 1
    db.commit()
    return 'OK'