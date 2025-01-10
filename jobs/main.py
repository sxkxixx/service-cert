import asyncio

from jobs import background_tasks


async def run_background_tasks() -> None:
    asyncio.create_task(background_tasks.generate_pages.init_generate_space())
    asyncio.create_task(background_tasks.generate_pages.generate_space())
    asyncio.create_task(background_tasks.generate_release_folder.create_release_folder())
