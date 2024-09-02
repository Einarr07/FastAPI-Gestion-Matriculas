from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..conexion import Base

class Matriculas(Base):
    __tablename__ = "matriculas"  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    id_materia = Column(Integer, ForeignKey("materias.id"), nullable=False)
    descripcion = Column(String(200), nullable=False)

    # Relación inversa con Estudiantes
    estudiante = relationship("Estudiantes", back_populates="matriculas")
    materia = relationship("Materias", back_populates="matriculas")
