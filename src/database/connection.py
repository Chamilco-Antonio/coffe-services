from sqlalchemy import create_engine
from pathlib import Path

# obtener el directorio actual
BASE_DIR = Path(__file__).parent 
DATABASE_FILE = BASE_DIR / "coffee.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"
# crear la instancia para la conexión a la BD
engine = create_engine(DATABASE_URL) 
