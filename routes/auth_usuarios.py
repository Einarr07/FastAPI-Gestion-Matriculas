from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.models.usuarios import Usuarios
from db.schemas.usuarios import CredencialesUsuario

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"Mensaje": "No encontrado"}}
)

def obtener_bd():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", status_code= status.HTTP_200_OK)
async def login(credentias: CredencialesUsuario, db: Session = Depends(obtener_bd)):

    usuario = db.query(Usuarios).filter(Usuarios.email == credentias.email).frist()

    contra = db.query(Usuarios).filter(Usuarios.password == credentias.password).firts()

    if not usuario and not contra:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Correo o contraseña incorrectos"

        )
    
    return {"Mensaje": "Inicio de sesión exitoso"}