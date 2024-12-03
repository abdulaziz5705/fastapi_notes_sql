import uuid

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(max_length=100)

class UserIn(UserBase):
    password: str = Field(min_length=1, max_length=100)
    confirm_password: str = Field(min_length=1, max_length=100)


class UserOut(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenUsername(BaseModel):
    username: str



class Login(BaseModel):
    username: str
    password: str
