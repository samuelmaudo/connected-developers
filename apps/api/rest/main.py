from fastapi import FastAPI

from apps.api.rest.connected import endpoints as connected
from modules.api.shared.infrastructure.containers import ApiContainer
from modules.shared.kernel.infrastructure.starters import TortoiseStarter

container = ApiContainer()
container.wire(modules=[connected])

app = FastAPI()
app.include_router(connected.router)


@app.on_event('startup')
async def start_tortoise() -> None:
    await TortoiseStarter(
        container.kernel.config.database.url(),
        container.tortoise_modules(),
        generate_schemas=True
    ).start()
