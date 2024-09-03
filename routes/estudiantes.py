from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.models.estudiantes import Estudiantes
from db.schemas.estudiantes import CrearEstudiante, ObtenerEstudiante, ActualizarEstudiante, EliminarEstudiante

router = APIRouter(
    prefix="/estudiantes",
    tags=["estuditantes"],
    responses={404: {"Mensaje": "No encontrado"}}
)

def obtener_bd():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code = status.HTTP_201_CREATED)
async def crear_estudiante(entrada: CrearEstudiante, db: Session = Depends(obtener_bd)):
    estudiante = Estudiantes(
        nombre = entrada.nombre,
        apellido = entrada.apellido,
        cedula = entrada.cedula,
        fecha_nacimiento = entrada.fecha_nacimiento,
        ciudad = entrada.ciudad,
        direccion = entrada.direccion,
        telefono = entrada.telefono,
        email = entrada.email
    )

    db.add(estudiante)

    try:
        db.commit()
        db.refresh(estudiante)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear estudiante: {e}")
    
    return estudiante

@router.get("/", response_model=list[ObtenerEstudiante], status_code=status.HTTP_200_OK)
async def obtener_estudiante(db: Session = Depends(obtener_bd)):
    estudiantes = db.query(Estudiantes).all()
    return estudiantes

@router.get("/{cedula}", response_model=ObtenerEstudiante, status_code=status.HTTP_200_OK)
async def cedula_estudiante(cedula: int, db: Session = Depends(obtener_bd)):
    estudiante = db.query(Estudiantes).filter_by(cedula=cedula).first()
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    
    return estudiante

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def actualizar_estudiante(id: int, entrada: ActualizarEstudiante, db: Session = Depends(obtener_bd)):
    try:
        estudiante = db.query(Estudiantes).filter_by(id=id).first()
        
        if not estudiante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")

        estudiante.nombre = entrada.nombre
        estudiante.apellido = entrada.apellido
        estudiante.cedula = entrada.cedula
        estudiante.fecha_nacimiento = entrada.fecha_nacimiento
        estudiante.ciudad = entrada.ciudad
        estudiante.direccion = entrada.direccion
        estudiante.telefono = entrada.telefono
        estudiante.email = entrada.email

        db.commit()
        db.refresh(estudiante)

        return estudiante

    except HTTPException as http_exc:
        # Este bloque solo se activa para excepciones HTTPException
        raise http_exc
    
    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el estudiante: {e}"
        )


@router.delete("/{cedula}", response_model=EliminarEstudiante, status_code=status.HTTP_200_OK)
async def eliminar_estudiante(cedula: int, db: Session = Depends(obtener_bd)):
    estudiante = db.query(Estudiantes).filter_by(cedula=cedula).first()
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")

    db.delete(estudiante)
    db.commit()
    respuesta = EliminarEstudiante(mensaje="Estudiante eliminado con exito")
    return respuesta

    