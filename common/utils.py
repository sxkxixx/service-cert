import uuid


def refer() -> str:
    return f'service-cert-{uuid.uuid4()}'
