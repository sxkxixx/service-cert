import enum


@enum.unique
class ServiceStatus(enum.Enum):
    # Creating space
    NEW = 'new'
    GENERATING_CONFLUENCE_SPACE = 'generating_confluence_space'

    # Creating folder for releases
    NEED_CREATE_RELEASE_FOLDER = 'need_create_release_folder'
    CREATING_RELEASE_FOLDER = 'creating_release_folder'

    # Updating homepage
    NEED_UPDATE_HOMEPAGE = 'need_update_homepage'

    # Ready
    READY = 'ready'


@enum.unique
class ReleaseStatus(enum.Enum):
    NEW = 'new'
    GENERATING_RELEASE_PAGE = 'generating_release_page'
    READY = 'ready'
