import pydantic


class AuthUser(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: pydantic.SecretStr
