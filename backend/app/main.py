from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.auth import routers as auth_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

# Route principale : redirige vers la doc
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
