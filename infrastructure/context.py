from contextvars import ContextVar

from common import clients

x_request_id = ContextVar('x-request-id')
method = ContextVar('method')
user_id = ContextVar('user-id')

confluence_client: ContextVar[clients.ConfluenceClient] = ContextVar('confluence-client')
