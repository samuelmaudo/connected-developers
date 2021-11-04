from typing import List

import orjson
import tortoise

__all__ = ('TortoiseStarter')


class TortoiseStarter:

    def __init__(
        self,
        db_url: str,
        model_modules: List[str],
        generate_schemas: bool = False
    ) -> None:
        self.db_url = db_url
        self.model_modules = model_modules
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
            db_url=self.db_url,
            modules={'models': self.model_modules})

    async def _maybe_generate_schema(self) -> None:
        if self.generate_schemas:
            await tortoise.Tortoise.generate_schemas()
