import databases
from sqlalchemy import create_engine, MetaData

#required to create a new DB with mysql on local session
SQLALCHEMY_DATABASE_URL = "mysql://root:nia@localhost:3306/gns3_rbac"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

