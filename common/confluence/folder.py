from common.schemas.folder import Folder
from infrastructure import context


async def create_folder(
    space_id: str,
    title: str,
    parent_id: str | None = None,
) -> Folder:
    confluence_client = context.confluence_client.get()
    response = await confluence_client.create_folder(
        space_id=space_id,
        title=title,
        parent_id=parent_id,
    )
    return Folder.model_validate(response.json())
