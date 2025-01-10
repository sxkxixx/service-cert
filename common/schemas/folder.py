import pydantic


class Folder(pydantic.BaseModel):
    id: str
    type: str
    parent_id: str = pydantic.Field(validation_alias='parentId')
