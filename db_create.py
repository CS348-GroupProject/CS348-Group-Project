from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///mydata.db', echo=True, isolation_level="SERIALIZABLE")
Base = declarative_base()

class Library(Base):
  __tablename__ = "Library"
  
  IBSN = Column(Integer, primary_key=True)
  Title = Column(String)
  
  def __repr__(self):
    return "{}".format(self.Title)
    
Base.metadata.create_all(engine)