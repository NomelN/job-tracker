from fastapi import FastAPI
from app.database import applications_collection
from app.auth import routers as auth_routes


app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def read_root():
    count = applications_collection.count_documents({})
    return {"message": f"Connexion MongoDB réussie. Nombre de candidatures : {count}"}