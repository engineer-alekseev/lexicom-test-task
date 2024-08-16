from fastapi import FastAPI
from app.api.endpoints.contacts import router as contacts_router

app = FastAPI()

app.include_router(contacts_router)