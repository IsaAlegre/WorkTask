from infrastructure.config import database_url
from infrastructure.persistence.db import create_tables

if __name__ == "__main__":
    create_tables(database_url())
    print("Tablas creadas")