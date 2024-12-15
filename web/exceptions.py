import fastapi_jsonrpc as jsonrpc


class ObjectDoesNotExistsError(jsonrpc.BaseError):
    CODE = -32001
    MESSAGE = 'Object does not exist'
