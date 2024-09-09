from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.schemas.usuarios import CrearUsuario, ObtenerUsuario
from db.models.usuarios import Usuarios
from passlib.context import CryptContext
from .auth_usuarios import obtener_usuario_actual

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

@router.get("/", response_model=list[ObtenerUsuario], status_code=status.HTTP_200_OK)
async def obtener_usuarios(db: Session = Depends(obtener_bd), usuario_actual: dict = Depends(obtener_usuario_actual)):
    usuarios = db.query(Usuarios).all()
    return usuarios

@router.get("/{id}", response_model=ObtenerUsuario, status_code=status.HTTP_200_OK)
async def id_usuarios(id: int, db: Session = Depends(obtener_bd), usuario_actual: dict = Depends(obtener_usuario_actual)):
    usuario = db.query(Usuarios).filter_by(id=id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return usuario