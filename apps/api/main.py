from fastapi import FastAPI

from apps.api.connected import urls as connected

app = FastAPI()
app.include_router(connected.router)
