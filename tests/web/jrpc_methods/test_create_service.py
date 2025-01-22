import dirty_equals


async def test_create_service(jrpc_client) -> None:
    params = {
        'service': {
            'name': 'Сервис аттестации релизов',
            'description': '120-3912-912321',
            'requirements': [],
        }
    }
    response = await jrpc_client(method='create_service_arbitrarily', params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'Сервис аттестации релизов',
        'description': '120-3912-912321',
        'confluence_page_link': None,
        'requirements': [],
    }


async def test_create_service_null_description(jrpc_client) -> None:
    params = {
        'service': {'name': 'Сервис аттестации релизов', 'description': None, 'requirements': []}
    }
    response = await jrpc_client(method='create_service_arbitrarily', params=params)
    assert response.success
    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'Сервис аттестации релизов',
        'description': None,
        'confluence_page_link': None,
        'requirements': [],
    }


async def test_create_service_with_requirements(jrpc_client) -> None:
    params = {
        'service': {
            'name': 'Сервис аттестации релизов',
            'description': None,
            'requirements': [
                {'name': 'Github', 'value': 'https://github.com/sxkxixx/service-cert'},
            ],
        },
    }
    response = await jrpc_client(method='create_service_arbitrarily', params=params)
    assert response.success

    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'Сервис аттестации релизов',
        'description': None,
        'confluence_page_link': None,
        'requirements': [
            {
                'id': dirty_equals.IsUUID(version=4),
                'name': 'Github',
                'value': 'https://github.com/sxkxixx/service-cert',
                'responsible_id': None,
                'type': None,
            },
        ],
    }


async def test_create_service_with_empty_requirement(jrpc_client) -> None:
    params = {
        'service': {
            'name': 'Сервис аттестации релизов',
            'description': None,
            'requirements': [
                {'name': 'Github', 'value': None},
            ],
        },
    }
    response = await jrpc_client(method='create_service_arbitrarily', params=params)
    assert response.success

    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'Сервис аттестации релизов',
        'description': None,
        'confluence_page_link': None,
        'requirements': [
            {
                'id': dirty_equals.IsUUID(version=4),
                'name': 'Github',
                'value': None,
                'responsible_id': None,
                'type': None,
            }
        ],
    }


async def test_create_service_with_multiple_requirements(jrpc_client) -> None:
    params = {
        'service': {
            'name': 'Сервис аттестации релизов',
            'description': None,
            'requirements': [
                {'name': 'Github', 'value': None},
                {'name': 'YouTrack', 'value': 'https://www.jetbrains.com/ru-ru/youtrack/'},
            ],
        },
    }
    response = await jrpc_client(method='create_service_arbitrarily', params=params)
    assert response.success

    assert response.result == {
        'id': dirty_equals.IsUUID(version=4),
        'name': 'Сервис аттестации релизов',
        'description': None,
        'confluence_page_link': None,
        'requirements': [
            {
                'id': dirty_equals.IsUUID(version=4),
                'name': 'Github',
                'value': None,
                'type': None,
                'responsible_id': None,
            },
            {
                'id': dirty_equals.IsUUID(version=4),
                'name': 'YouTrack',
                'value': 'https://www.jetbrains.com/ru-ru/youtrack/',
                'responsible_id': None,
                'type': None,
            },
        ],
    }
