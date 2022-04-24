from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    gender: str  # maybe bool :)
    imageUrl: Optional[str]
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class Player(UserBase):
    count_of_session: int
    count_of_wins: int
    count_of_fails: int
    sec_in_game: int

class ImageUrl(BaseModel):
    imageUrl: str
