from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL
URL_DATABASE='mysql+pymysql://root:@localhost:3306/productapp'

# Create the SQLAlchemy engine
engine=create_engine(URL_DATABASE)

# Create a sessionmaker object for the database session
SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

# Base class for SQLAlchemy models
Base =declarative_base()
