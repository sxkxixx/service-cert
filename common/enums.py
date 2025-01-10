import enum


@enum.unique
class ServiceStatus(enum.Enum):
    NEW = 'new'
    GENERATING_CONFLUENCE_SPACE = 'generating_confluence_space'

    # Creating folder for releases
    NEED_CREATE_RELEASE_FOLDER = 'need_create_release_folder'
    CREATING_RELEASE_FOLDER = 'creating_release_folder'

    # Updating homepage
    NEED_UPDATE_HOMEPAGE = 'need_update_homepage'

    # Ready
    READY = 'ready'
