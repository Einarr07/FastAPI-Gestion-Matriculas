from pydantic import BaseModel

class CrearMatricula(BaseModel):
    id_estudiante: int
    id_materia: int
    descripcion: str

class ObtenerMatricula(BaseModel):
    id: int
    id_estudiante: int
    id_materia: int
    descripcion: str

class ActualizarMatricula(BaseModel):
    id_estudiante: int
    id_materia: int
    descripcion: str

class EliminarMatricula(BaseModel):
    mensaje: str
