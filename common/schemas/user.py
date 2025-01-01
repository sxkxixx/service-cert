import uuid

import pydantic


class RegisterUser(pydantic.BaseModel):
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    password: str


class UserResponse(pydantic.BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: pydantic.EmailStr


class UserLoginRequest(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str
