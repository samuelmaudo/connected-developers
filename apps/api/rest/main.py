from fastapi import FastAPI

from apps.api.rest.connected import urls as connected
from modules.shared.kernel.infrastructure.starters import (
    DotEnvStarter,
    TortoiseStarter
)

dotenv = DotEnvStarter()
tortoise = TortoiseStarter()

app = FastAPI()
app.include_router(connected.router)
app.add_event_handler('startup', dotenv.start)
app.add_event_handler('startup', tortoise.start)
