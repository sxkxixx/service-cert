import pydantic


class ConfluenceSpaceResponse(pydantic.BaseModel):
    id: int
    key: str
    alias: str
    name: str
    homepage: dict
    links: dict = pydantic.Field(validation_alias='_links')

    @pydantic.computed_field()
    @property
    def webui_url(self) -> str:
        return f'{self.links["base"]}{self.links["webui"]}'

    @pydantic.computed_field()
    @property
    def homepage_id(self) -> int:
        return self.homepage['id']
