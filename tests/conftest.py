import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.database import Base, get_db  # Cambia esto por la ruta real de tu Base

# 1. Importamos tu app de FastAPI, el get_db real y tu Base de SQLAlchemy
from main import app

# 2. Configurar la Base de Datos de Pruebas (SQLite en memoria)
# 'StaticPool' permite que la base de datos persista en la misma conexión durante el test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 3. Crear la función get_db alternativa para los tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# 4. Configurar las Fixtures de Pytest
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Crea las tablas antes de cada test y las destruye al finalizar."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def customer():
    """Inyecta el override en la app y expone el cliente de pruebas."""
    # Le decimos a FastAPI que reemplace la dependencia real por la de pruebas
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    # Limpiamos los overrides al terminar para no afectar a otros módulos
    app.dependency_overrides.clear()
