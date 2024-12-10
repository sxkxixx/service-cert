import pydantic


class BatchQuery(pydantic.BaseModel):
    limit: pydantic.PositiveInt
    offset: pydantic.NonNegativeInt
