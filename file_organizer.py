import argparse
import asyncio
import logging as log
from aiopath import AsyncPath
from aioshutil import copyfile

log.basicConfig(level=log.INFO)


async def copy_file(file_path: AsyncPath, dest_dir: AsyncPath):
    try:
        extension = file_path.suffix.lower()
        dest_subdir = dest_dir / extension.strip('.')
        await dest_subdir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_subdir / file_path.name
        await copyfile(file_path, dest_file)
        log.info(f'File {file_path.name} copied to {dest_subdir}')
    except Exception as e:
        log.error(f"Copying error of {file_path} to {dest_subdir}: {e}")


async def read_dir(source_dir: AsyncPath, dest_dir: AsyncPath):
    tasks = []
    async for path in source_dir.rglob('*'):
        if await path.is_file():
            tasks.append(copy_file(path, dest_dir))
    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description='Asynchronous copying and organising of files based on extension')
    parser.add_argument('source', help='Source directory')
    parser.add_argument('destination', help='Destination directory')
    args = parser.parse_args()

    source_dir = AsyncPath(args.source)
    dest_dir = AsyncPath(args.destination)

    asyncio.run(read_dir(source_dir, dest_dir))


if __name__ == '__main__':
    main()
