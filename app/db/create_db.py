from sqlalchemy.schema import MetaData
from sqlalchemy.engine import Engine

def create_db(engine:Engine) -> None:
    meta_data = MetaData(bind=engine) 
    meta_data.create_all(bind=engine)