from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conexion import session_local
from db.models.matriculas import Matriculas
from db.schemas.matriculas import CrearMatricula, ObtenerMatricula, ActualizarMatricula, EliminarMatricula

router = APIRouter(
    prefix="/matriculas",
    tags=["matriculas"],
    responses={404: {"Mensaje": "No encontrado"}}
)

def obtener_bd():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code = status.HTTP_201_CREATED)
async def crear_matricula(entrada: CrearMatricula, db: Session = Depends(obtener_bd)):
    matricula = Matriculas(
        id_estudiante = entrada.id_estudiante,
        id_materia = entrada.id_materia,
        descripcion = entrada.descripcion
    )

    db.add(matricula)

    try:
        db.commit()
        db.refresh(matricula)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la matricula: {e}")
    
    return matricula

@router.get("/", response_model=list[ObtenerMatricula], status_code = status.HTTP_200_OK)
async def obtener_matriculas(db: Session = Depends(obtener_bd)):
    matriculas = db.query(Matriculas).all()
    return matriculas

@router.get("/{id}", response_model=ObtenerMatricula, status_code = status.HTTP_200_OK)
async def id_matricula(id: int, db: Session = Depends(obtener_bd)):
    try:
        matricula = db.query(Matriculas).filter_by(id = id).first()
        if not matricula:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La matricula no existe")
        
        return matricula
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener matrucla: {e}"
        )
    

@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED)
async def actualizar_matricula(id: int, entrada: ActualizarMatricula, db: Session = Depends(obtener_bd)):
    try:
        matricula = db.query(Matriculas).filter_by(id=id).first()
        if not matricula:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La matricula no existe")
        
        matricula.id_estudiante = entrada.id_estudiante
        matricula.id_materia = entrada.id_materia
        matricula.descripcion = entrada.descripcion

        db.commit()
        db.refresh(matricula)

        return matricula
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener matrucla: {e}"
        )

@router.delete("/{id}", response_model=EliminarMatricula, status_code=status.HTTP_200_OK)
async def eliminar_matricula(id: int, db: Session = Depends(obtener_bd)):
    try: 
        matricula = db.query(Matriculas).filter_by(id = id).first()
        if not matricula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Matricula no encontrada"
                )
        
        db.delete(matricula)
        db.commit()
        
        respuesta = EliminarMatricula(mensaje="Matricula eliminada exitosamente")
        return respuesta

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la matricula: {e}"
        )
