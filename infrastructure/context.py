from contextvars import ContextVar

x_request_id = ContextVar('x-request-id')
method = ContextVar('method')
user_id = ContextVar('user-id')
