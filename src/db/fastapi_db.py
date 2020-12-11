from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#required to create a new DB with mysql on local session
SQLALCHEMY_DATABASE_URL = "mysql://root:nia@localhost:3306/gns3_rbac"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()