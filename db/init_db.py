from database import Base, engine, Session
from models import User

# create database with tables
Base.metadata.create_all(bind=engine)
