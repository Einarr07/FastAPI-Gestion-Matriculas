from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from ..conexion import Base

class Matriculas(Base):
    __tablename__ = "matriculas"  
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_estudiante = Column(BigInteger, ForeignKey("estudiantes.id"), nullable=False)
    id_materia = Column(BigInteger, ForeignKey("materias.id"), nullable=False)
    descripcion = Column(String(200), nullable=False)

    # Relación inversa con Estudiantes
    estudiante = relationship("Estudiantes", back_populates="matriculas")
    materia = relationship("Materias", back_populates="matriculas")
