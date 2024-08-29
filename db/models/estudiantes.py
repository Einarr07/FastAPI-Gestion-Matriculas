from sqlalchemy import Column, Integer, String,BigInteger, Date
from sqlalchemy.orm import relationship
from ..conexion import Base

class Estudiantes(Base):
    __table__  = "estudiantes"
    id = Column(Integer(11), primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    cedula = Column(BigInteger(11), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    ciudada = Column(String(20), nullable=False)
    direccion = Column(String(20), nullable=False)
    telefono = Column(String(10), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)

    usuarios = relationship("Usuarios", back_populates="estudiantes")