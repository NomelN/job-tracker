from fastapi import FastAPI
from app.database import applications_collection

app = FastAPI()


@app.get("/")
def read_root():
    count = applications_collection.count_documents({})
    return {"message": f"Connexion MongoDB réussie. Nombre de candidatures : {count}"}