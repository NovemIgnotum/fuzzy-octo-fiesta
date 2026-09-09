from fastapi import FastAPI

app = FastAPI(
    title="Read and send",
    description="Extrait les informations d'un PDF et programme l'envoie de message selon les événements.",
    version="1.0"
)

@app.get("/")
def home():
    return {"message" : "Welcome to the Read and Send API"}

@app.get("/ping")
def ping(): 
    return {"status" : "success", 'message': "Pong"}