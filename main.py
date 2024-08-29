from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI(
    responses={404: {"Mensaje": "No encontrado"}}
)

@app.get("/")
def main():
    "Redireccionamiento a la documentación de la API"
    return RedirectResponse(url="/docs/")