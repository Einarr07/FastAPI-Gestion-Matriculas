from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.orm import relationship
from ..conexion import Base

class Materias(Base):
    __tablename__ = "materias"  
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    codigo = Column(Integer, nullable=False, unique=True)
    descripcion = Column(String(200), nullable=False)
    creditos = Column(Integer, nullable=False)

    # Importación diferida de Matriculas
    from .matriculas import Matriculas  # Importar aquí para evitar ciclo
    matriculas = relationship("Matriculas", back_populates="materia")
