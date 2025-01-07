import uuid

import pydantic


class RegisterUser(pydantic.BaseModel):
    name: str
    nickname: str
    email: pydantic.EmailStr
    password: str


class UserResponse(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    nickname: str
    email: pydantic.EmailStr


class UserLoginRequest(pydantic.BaseModel):
    first_factor: str
    password: str
