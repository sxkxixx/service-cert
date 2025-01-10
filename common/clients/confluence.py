import typing

import httpx


class ConfluenceClient:
    def __init__(self, base_url: str, email: str, api_token: str):
        self._base_url = base_url  # https://{your-domain}
        self._basic_auth = httpx.BasicAuth(username=email, password=api_token)
        self._default_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    async def create_space(
        self,
        name: str,
        key: str | None = None,
        alias: str | None = None,
        description: dict | None = None,
        permissions: list[typing.Any] | None = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient(
            base_url=self._base_url,
            auth=self._basic_auth,
            headers=self._default_headers,
        ) as client:
            response = await client.post(
                url='/wiki/rest/api/space',
                json={
                    'name': name,
                    'key': key,
                    'alias': alias,
                    'description': description,
                    'permissions': permissions,
                },
            )
        return response

    async def get_page_info(self, id_: int | str) -> httpx.Response:
        async with httpx.AsyncClient(
            base_url=self._base_url,
            auth=self._basic_auth,
            headers=self._default_headers,
        ) as client:
            return await client.get(url=f'/wiki/rest/api/content/{id_}')

    async def edit_page(
        self,
        page_id: int | str,
        *,
        version: int,
        title: str,
        type_: str,  # page
        status: str,  # current
        **kwargs,
    ) -> httpx.Response:
        async with httpx.AsyncClient(
            base_url=self._base_url,
            auth=self._basic_auth,
            headers=self._default_headers,
        ) as client:
            return await client.put(
                url=f'/wiki/rest/api/content/{page_id}',
                json=kwargs,
            )

    async def create_page(
        self,
        space_id: int,
        status: str,
        title: str,
        parent_id: str | None = None,
        representation_content: dict | None = None,
    ):
        # POST https://asemyonov.atlassian.net/wiki/api/v2/pages
        pass

    async def create_folder(
        self,
        space_id: str,
        title: str,
        parent_id: str | None = None,
    ):
        # https://asemyonov.atlassian.net/wiki/api/v2/folders
        async with httpx.AsyncClient(
            base_url=self._base_url,
            auth=self._basic_auth,
            headers=self._default_headers,
        ) as client:
            response = await client.post(
                url='/wiki/api/v2/folders',
                json={
                    'spaceId': space_id,
                    'title': title,
                    'parentId': parent_id,
                },
            )
        return response
