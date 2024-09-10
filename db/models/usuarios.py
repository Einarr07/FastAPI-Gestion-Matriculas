from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from ..conexion import Base

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(20))
    apellido = Column(String(20), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
