import os

import dotenv
import orjson
import tortoise

__all__ = ('DotEnvStarter', 'TortoiseStarter')


class DotEnvStarter:

    async def start(self) -> None:
        dotenv.load_dotenv()


class TortoiseStarter:

    def __init__(self, generate_schemas: bool = False) -> None:
        self.generate_schemas = generate_schemas

    async def start(self) -> None:
        await self._replace_json_library()
        await self._init_tortoise()
        await self._maybe_generate_schema()

    async def _replace_json_library(self) -> None:
        tortoise.fields.data.JSON_DUMPS = lambda s: orjson.dumps(s).decode('utf-8')
        tortoise.fields.data.JSON_LOADS = orjson.loads

    async def _init_tortoise(self) -> None:
        await tortoise.Tortoise.init(
            db_url=os.getenv('DATABASE_URL'),
            modules={'models': ['modules.api.connected.infrastructure.repositories']}
        )

    async def _maybe_generate_schema(self) -> None:
        if self.generate_schemas:
            await tortoise.Tortoise.generate_schemas()
