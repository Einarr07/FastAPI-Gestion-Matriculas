from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..conexion import Base

class Usuarios(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    nombre = Column(String(20),  )
    apellido = Column(String(20), nullable=False )
    email = Column(String(30), unique=True ,nullable=False)
    password = Column(String(20), nullable=False)
    id_estudiante = Column(Integer(11), ForeignKey("estudiantes.id"),unique=True,nullable=False)

    id_estudiante = relationship("Estudiantes", back_populates="usuarios")