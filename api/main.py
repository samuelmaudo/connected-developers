from fastapi import FastAPI

from api.connected.application import urls as connected

app = FastAPI()
app.include_router(connected.router)
