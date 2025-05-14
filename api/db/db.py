from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db.models import Base
import os

# Configuración del URI de la base de datos (SQLite en disco)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///clinic.db")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear todas las tablas si no existen
Base.metadata.create_all(bind=engine)

# Crear la sesión
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = Session()
