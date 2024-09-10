from sqlalchemy import Column, String, BigInteger, Date
from sqlalchemy.orm import relationship
from ..conexion import Base

class Estudiantes(Base):
    __tablename__ = "estudiantes"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    cedula = Column(BigInteger, nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    ciudad = Column(String(20), nullable=False)  
    direccion = Column(String(50), nullable=False)
    telefono = Column(String(10), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    
    usuarios = relationship("Usuarios", back_populates="estudiantes")
    matriculas = relationship("Matriculas", back_populates="estudiante")
