from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("postgresql+psycopg2://postgres:0000@localhost/bankdb")
sessionLocal= sessionmaker(bind=engine)