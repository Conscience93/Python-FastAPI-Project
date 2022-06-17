"""Following FastAPI SQL (Relational) database convention"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLACADEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLACADEMY_DATABASE_URL = 'postgresql://postgres:UNMC1234@localhost/fastapi'

engine = create_engine(SQLACADEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

''' Previous usage of psycopg2
import psycopg2
import time
while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='UNMC1234', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(3)'''