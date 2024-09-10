# Gestión de matriculas con FastAPI y MYSQL

## Descripción del proyecto
Este proyecto es una aplicación web para gestionar matrículas de estudiantes en diversas materias utilizando FastAPI y MySQL. Permite la creación de usuarios, así como la gestión de estudiantes, materias y sus respectivas matrículas. Es ideal para instituciones educativas que desean un sistema sencillo y eficaz para administrar la información de sus estudiantes y cursos.

## Modelo de la Base de datos
Este es el diagrama de la base de datos utilizado para este proyecto.

## Estructura del proyecto
- app/
  - main.py          # Archivo principal de la aplicación
  - db
    - models.py        # Definición de los modelos de datos con SQLAlchemy
    - schemas.py       # Definición de los esquemas de Pydantic para validación de datos
  - routers/
    - usuarios.py    # Endpoints relacionados con la gestión de usuarios
    - estudiantes.py # Endpoints relacionados con la gestión de estudiantes
    - materias.py    # Endpoints relacionados con la gestión de materias
    - matriculas.py  # Endpoints relacionados con la gestión de matrículas
    - auth_usuarios.py # Endpoints relacionados con la autenticación de los usuarios

### Instrucciones de instalación y configuración

#### Crear un entorno virtual

Para la creación de un entorno virtual deberemos tener Python previamente instalado y ejecutar el siguiente comando:

```bash
virtualenv -p python env
```

Una vez hayamos creado nuestro entorno virtual nos moveremos dentro de este con el siguiente comando:

```bash
.\env\Scripts\activate
```

Cuando ya nos encontremos dentro de este podremos instalar todas las bibliotecas que vayamos a necesitar en nuestro proyecto
y crearemos un archivo requirements.txt donde se encontrarán todas las dependencias de nuestro proyecto.
Para crearlo necesitaremos el siguiente comando:

```bash
pip freeze > requirements.txt
```

Y en caso de que necesitemos instalar las dependencias de otro entorno virtual lo haremos mediante el siguiente comando:

```bash
pip install -r requirements.txt
```

Finalmente, para salir del entorno virtual que hemos creado utilizaremos 

```bash
deactivate
```
#### Activación del servidor 

Para poder utilizar FastAPI necesitaremos un servidor ASGI (Asynchronous Server Gateway Interface), el cual es
una especificación para servidores web y frameworks web en  Python que permite la comunicación asincrónica entre 
servidores web y aplicaciones web.

```bash
pip install "uvicorn[standard]"
```

para correr el servidor deberemos ingresar el siguiente comando:

```bash
uvicorn main:app --reload
```
### Créditos
Desarrollado por Mateo Congo