from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from ..conexion import Base

class Materias(Base):
    __table__ = "materias"
    id = Column(Integer(11), primary_key=True, index=True ,autoincrement=True)
    nombre = Column(String(20), nullable=False)
    codigo = Column(Integer(11), nullable=False)
    descripcion = Column(String(200), nullable=False)
    creditos = Column(Integer(5), nullable=False)

    matriculas = relationship("Matriculas", back_populates="materias")