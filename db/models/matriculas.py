from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..conexion import Base

class Matricualas(Base):
    __table__ = "matriculas"
    id = Column(Integer(11), primary_key=True, index=True, autoincrement=True)
    id_estudiante = Column(Integer(11), ForeignKey=("estudiantes.id"), nullable=False)
    id_materia = Column(Integer(11), ForeignKey=("materias.id"), nullable=False)
    descripcion = Column(String(200), nullable=False)

    estudiante = relationship("Estudiantes", back_populates="matriculas")
    materia = relationship("Materias", back_populates="matriculas")