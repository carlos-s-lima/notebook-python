import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DB_NAME = "meu_banco.db"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, DB_NAME)}"

engine = create_engine(
    DATABASE_URL,
    # Este argumento é CRÍTICO para SQLite em aplicações desktop, pois o SQLite por padrão só permite
    # conexões do mesmo thread que criou a engine. Como em aplicações desktop você pode ter múltiplas
    # threads interagindo com o banco de dados, precisamos desabilitar essa verificação
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,   
    bind=engine        
)


Base = declarative_base()