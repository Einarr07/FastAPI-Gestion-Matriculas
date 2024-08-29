from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Cargar las variables de entorno desde el .env
load_dotenv()

#Obtener la URL de la base de datos desde las variables de entorno
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}"

# Verificamos que la DATABASE_URL se cargó correctamente
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL no esta configurado en el archivo .env")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear la sesión local
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar la base
Base = declarative_base()

