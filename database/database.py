from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Ruta de tu base de datos local SQLite
# El archivo "sql_app.db" se creará automáticamente en la raíz de tu proyecto
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Crear el motor de conexión (Engine)
# 'connect_args={"check_same_thread": False}' es EXCLUSIVO de SQLite.
# Permite que FastAPI use múltiples hilos para consultar la BD de forma segura.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Crear una fábrica de sesiones (SessionLocal)
# Cada vez que una API pida datos, esta fábrica le dará una conexión única.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Crear la clase Base para el ORM
# Todos nuestros modelos futuros (Tablas) heredarán de esta clase Base.
Base = declarative_base()

# 5. Dependencia para FastAPI (Generador de Sesiones)
# Abre una conexión por cada petición HTTP y se asegura de cerrarla al terminar.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
