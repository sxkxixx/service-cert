import uuid

import pydantic


class Teammate(pydantic.BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
