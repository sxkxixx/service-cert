import fastapi_jsonrpc as jsonrpc


class ObjectDoesNotExistsError(jsonrpc.BaseError):
    CODE = -32001
    MESSAGE = 'Object does not exist'


class AlreadyExistsError(jsonrpc.BaseError):
    CODE = -32002
    MESSAGE = 'Object already exists'


class AuthenticationError(jsonrpc.BaseError):
    CODE = -32003
    MESSAGE = 'Authentication failed'
