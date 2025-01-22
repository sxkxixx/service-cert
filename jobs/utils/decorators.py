import asyncio
import functools
import logging
import typing

logger = logging.getLogger(__name__)


def periodic_task_run(sleep: int | None):
    def _periodic_task_run(coro: typing.Callable):
        @functools.wraps(coro)
        async def _wrapper(*args, **kwargs):
            if not sleep:
                logger.info('Запущена job "%s": один запуск', coro.__name__)
                return await coro(coro, *args, **kwargs)

            while True:
                logger.info('Запущена job "%s"', coro.__name__)
                await asyncio.sleep(delay=sleep)
                await coro(coro, *args, **kwargs)

        return _wrapper

    return _periodic_task_run
