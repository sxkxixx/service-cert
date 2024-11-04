from logging import config as logging_config

__all__ = [
    'setup_logging',
]


def setup_logging():
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {'default': {'()': 'infrastructure.logging.json_formatter.JsonFormatter'}},
        'handlers': {'default': {'class': 'logging.StreamHandler', 'formatter': 'default'}},
        'loggers': {
            '': {
                'level': 'INFO',
                'handlers': ['default'],
            },
            'aiohttp.server': {
                'level': 'INFO',
                'handlers': ['default'],
            },
            'aiohttp.web': {
                'level': 'INFO',
                'handlers': ['default'],
            },
        },
    }

    logging_config.dictConfig(config)
