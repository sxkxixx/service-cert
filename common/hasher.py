from passlib.context import CryptContext

_crypto_context = CryptContext(schemes=['sha256_crypt'])

__all__ = [
    'get_password_hash',
    'verify_password',
]


def get_password_hash(password: str) -> str:
    return _crypto_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return _crypto_context.verify(secret=plain_password, hash=hash_password)
