import datetime
import json
from logging import Formatter, LogRecord

from infrastructure import context


class JsonFormatter(Formatter):
    def format(self, record: LogRecord):
        data = {
            '@message': record.getMessage(),
            '@x-request-id': context.x_request_id.get(None),
            '@user-id': context.user_id.get(None),
        }
        message = {
            '@timestamp': datetime.datetime.now().isoformat(),
            '@data': data,
            '@logger': record.name,
            '@level': record.levelname.upper(),
        }
        if record.exc_text:
            message['exception'] = record.exc_text
        if record.stack_info:
            message['stack_trace'] = self.formatStack(record.stack_info)
        return json.dumps(message, ensure_ascii=False)
