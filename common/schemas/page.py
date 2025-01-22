import pydantic


class Page(pydantic.BaseModel):
    id: str
    links: dict = pydantic.Field(validation_alias='_links')

    @pydantic.computed_field()
    @property
    def webui_url(self) -> str:
        return f'{self.links["base"]}{self.links["webui"]}'
