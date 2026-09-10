from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import connect_to_mongodb, close_mongodb_connection
from app.routes import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()

app = FastAPI(
    title="Read and send",
    description="Extrait les informations d'un PDF et programme l'envoie de message selon les événements.",
    version="1.0",
    lifespan=lifespan
)

app.include_router(users.router, prefix="/api/user", tags=["users"])
@app.get("/")
def home():
    return {"message" : "Welcome to the Read and Send API"}

@app.get("/ping")
def ping(): 
    return {"status" : "success", 'message': "Pong"}