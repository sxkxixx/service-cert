from common import db
from common.schemas.page import Page
from infrastructure import context
from services.release_requirements import selectors as rr_selectors


async def create_page(
    release: db.Release,
    service_space: db.ServiceSpace,
) -> Page:
    confluence_client = context.confluence_client.get()
    release_requirements = await rr_selectors.get_release_requirement_by_release_id(
        release_id=release.id
    )
    representation = get_release_page_representation(
        release=release, requirements=release_requirements, teammates=[]
    )
    response = await confluence_client.create_page(
        space_id=str(service_space.ext_id),
        status='current',
        title=release.name,
        parent_id=service_space.release_folder_id,
        representation_content={
            'representation': 'wiki',
            'value': representation,
        },
    )
    return Page.model_validate(response)


def get_release_page_representation(
    release: db.Release,
    requirements: list[db.ReleaseRequirement],
    teammates: list[db.User],
) -> str:
    result = f'# {release.name}\n\n|\t|\t|\n|----|----|\n'

    mates = '\n'.join([mate.name for mate in teammates])
    if not mates:
        mates = '-'
    result += f'|Команда|{mates}|\n'

    for req in requirements:
        result += f'|{req.name}|{req.value if req.value else "-"}|'
    return result
