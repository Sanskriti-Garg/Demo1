from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Define your MSSQL connection string
DATABASE_URL = 'mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server'

# Create SQLAlchemy engine and metadata
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData(bind=engine)

# Define Base class using declarative_base
Base = declarative_base(metadata=metadata)

# Define Film table
class Film(Base):
    __tablename__ = 'Film'

    flim_id = Column(Integer, primary_key=True, autoincrement=True)
    flim_title = Column(String(255), nullable=False)

# Define FilmActor table
class FilmActor(Base):
    __tablename__ = 'FilmActor'

    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    film_name = Column(String(255), nullable=False)
    flim_id = Column(Integer, ForeignKey('Film.flim_id'), nullable=False)

# Create tables in the database
Base.metadata.create_all()

print("Tables created successfully.")
