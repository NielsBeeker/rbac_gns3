import databases
import sqlalchemy

#required to create a new DB with mysql on local session
SQLALCHEMY_DATABASE_URL = "mysql://root:nia@localhost:3306/gns3_rbac"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)

metadata.create_all(engine)

