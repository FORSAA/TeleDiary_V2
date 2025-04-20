from Parser.libs.filesManagerLibs import *

class FilesManager():

    ABS_BASE_DIR:str = __file__
    TEMP_FILES_DIR:str = Path(ABS_BASE_DIR) / 'temp'

    @staticmethod
    async def make_dir(*paths: tuple[str, str]):
        async def create_dir(dir_path: str, dir_name: str):
            path = Path(dir_path) / dir_name
            await asyncio.to_thread(makedirs, path)

        await asyncio.gather(*(create_dir(p, n) for p, n in paths))

    @staticmethod
    async def make_dirs(dir_path:str):
        await asyncio.to_thread(makedirs, dir_path)

    @staticmethod
    async def rmtree(dir_path:str):
        await asyncio.to_thread(rmtree, dir_path)

    @staticmethod
    async def abs_path(addition:str='') -> str:
        return Path(FilesManager.ABS_BASE_DIR) / addition
    
    @staticmethod
    async def list_dir(dir_path:str) -> list[str]:
        return await asyncio.to_thread(listdir, dir_path)
    
    @staticmethod
    async def is_file(path:str) -> bool:
        return await asyncio.to_thread(isfile, path)

    @staticmethod
    async def check_existance(path:str) -> bool:
        return await asyncio.to_thread(exists, path)

    @staticmethod
    async def remove_file(path:str) -> None:
        await asyncio.to_thread(remove, path)

    @staticmethod
    async def clear_dir(*dir_paths: str) -> None:
        tasks = []

        for dir_path in dir_paths:
            if not await FilesManager.check_existance(dir_path):
                print(f'not found: {dir_path}')
                continue

            items = await FilesManager.list_dir(dir_path)

            for item in items:
                item_path = Path(dir_path) / item

                if await FilesManager.is_file(item_path):
                    tasks.append(
                        asyncio.create_task(
                            asyncio.to_thread(remove, item_path)
                        )
                    )
                else:
                    tasks.append(
                        asyncio.create_task(
                            asyncio.to_thread(rmtree, item_path)
                        )
                    )

        await asyncio.gather(*tasks, return_exceptions=False)
