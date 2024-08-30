from sqlalchemy import Column, String, ForeignKey, BigInteger, Integer
from sqlalchemy.orm import relationship
from ..conexion import Base
from .estudiantes import Estudiantes

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(20))
    apellido = Column(String(20), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    id_estudiante = Column(BigInteger, ForeignKey("estudiantes.id"))

    estudiantes = relationship("Estudiantes", back_populates="usuarios")
