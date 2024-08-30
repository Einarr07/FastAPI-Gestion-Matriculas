from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.models.usuarios import Usuarios
from db.schemas.usuarios import CredencialesUsuario
from passlib.context import CryptContext

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contraseña(contraseña_plana: str, contraseña_encriptada: str) -> bool:
    return pwd_context.verify(contraseña_plana, contraseña_encriptada)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credenciales: CredencialesUsuario, db: Session = Depends(obtener_bd)):

    usuario = db.query(Usuarios).filter(Usuarios.email == credenciales.email).first()

    if not usuario or not verificar_contraseña(credenciales.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    
    return {"Mensaje": "Inicio de sesión exitoso"}
