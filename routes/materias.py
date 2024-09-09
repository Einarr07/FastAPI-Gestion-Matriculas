from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.models.materias import Materias
from db.schemas.materias import CrearMateria, ObtenerMateria, ActualizarMatria, EliminarMateria
from .auth_usuarios import obtener_usuario_actual

router = APIRouter(
    prefix="/materias",
    tags=["materias"],
    responses={404: {"Mensaje": "No encontrado"}}
)

def obtener_bd():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code= status.HTTP_201_CREATED)
async def crear_materia(entrada: CrearMateria, db: Session = Depends(obtener_bd), usuario_actual: dict = Depends(obtener_usuario_actual)):
    materia = Materias(
        nombre = entrada.nombre,
        codigo = entrada.codigo,
        descripcion = entrada.descripcion,
        creditos = entrada.creditos
    )

    db.add(materia)

    try:
        db.commit()
        db.refresh(materia)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la materia")
    
    return materia

@router.get("/", response_model=list[ObtenerMateria], status_code=status.HTTP_200_OK)
async def obtener_materia(db: Session = Depends(obtener_bd), usuario_actual: dict = Depends(obtener_usuario_actual)):
    try:
        materias = db.query(Materias).all()
        return materias
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener materia: {e}"
        )
    
@router.get("/{codigo}", response_model=ObtenerMateria, status_code=status.HTTP_200_OK)
async def id_materia(codigo: int, db: Session = Depends(obtener_bd), usuario_actual: dict = Depends(obtener_usuario_actual)):
    try:
        materia = db.query(Materias).filter_by(codigo=codigo).first()
        if not materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materia no encontrada")
    
        return materia
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener materia: {e}"
        )

@router.put("/{codigo}", response_model=ObtenerMateria, status_code=status.HTTP_202_ACCEPTED)
async def actualizar_materia(codigo: int, entrada: ActualizarMatria, db: Session = Depends(obtener_bd), usuario_actual: dict = Depends(obtener_usuario_actual)):
    try:
        materia = db.query(Materias).filter_by(codigo=codigo).first()
        if not materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materia no encontrada")

        materia.nombre = entrada.nombre
        materia.codigo = entrada.codigo
        materia.descripcion = entrada.descripcion
        materia.creditos = entrada.creditos
        db.commit()
        db.refresh(materia)

        return materia
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar materia: {e}"
        )

@router.delete("/{codigo}", response_model=EliminarMateria, status_code=status.HTTP_200_OK)
async def eliminar_materia(codigo:int, db: Session = Depends(obtener_bd), usuario_actual: dict = Depends(obtener_usuario_actual)):
    try:
        materia = db.query(Materias).filter_by(codigo=codigo).first()
        if not materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materia no encontrada")
        
        db.delete(materia)
        db.commit()
        respuesta = EliminarMateria(mensaje="Materia eliminada exitosamente")
        return respuesta
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar materia: {e}"
        )