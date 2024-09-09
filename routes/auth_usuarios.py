from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.models.usuarios import Usuarios
from db.schemas.usuarios import Token, ObtenerUsuario
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
import os
from dotenv import load_dotenv

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"Mensaje": "No encontrado"}}
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Secret_key no está configurada en el archivo .env")

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_bd():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def verificar_contraseña(contraseña_plana: str, contraseña_encriptada: str) -> bool:
    return pwd_context.verify(contraseña_plana, contraseña_encriptada)

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(obtener_bd)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error al decodificar el token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Verificar existencia del usuario
    usuario = db.query(Usuarios).filter(Usuarios.email == email).first()
    if usuario is None:
        raise credentials_exception
    return usuario


@router.post("/login", response_model=Token, status_code= status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(obtener_bd)):
    usuario = db.query(Usuarios).filter(Usuarios.email == form_data.username).first()

    if not usuario or not verificar_contraseña(form_data.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_token_acceso(
        data={"sub": usuario.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/usuarios/yo", response_model=ObtenerUsuario)
async def leer_usuarios_me(usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    try:
        return usuario_actual
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obtener estudiantes: {e}"
        )
