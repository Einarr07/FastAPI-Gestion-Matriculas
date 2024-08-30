from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.schemas.usuarios import CrearUsuario, ObtenerUsuario
from db.models.usuarios import Usuarios
from passlib.context import CryptContext

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"Mensaje": "No encontrado"}}
)

def obtener_bd():
    
    db = session_local()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encriptar_contraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)

@router.post("/", response_model=ObtenerUsuario, status_code=status.HTTP_201_CREATED)
async def crear_usuario(entrada: CrearUsuario, db: Session = Depends(obtener_bd)):
    usuario = Usuarios(
        nombre = entrada.nombre,
        apellido = entrada.apellido,
        email = entrada.email,
        password = encriptar_contraseña(entrada.password)
    )

    db.add(usuario)

    try:
        db.commit()
        db.refresh(usuario)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear al usuario")
    
    return usuario