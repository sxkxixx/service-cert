import uuid


def request_id() -> str:
    return f'service-cert-{uuid.uuid4()}'
