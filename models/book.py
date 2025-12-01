from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db_session import Base

class Book(Base):
    __tablename__ = "Books"

    Id = Column(Integer, primary_key=True, index=True)
    Title = Column(String(200), nullable=False)
    Author = Column(String(200), nullable=False)
    Description = Column(String, nullable=True)
    PdfUrl = Column(String(500), nullable=True)
    CoverUrl = Column(String(500), nullable=True)
    CreatedAt = Column(DateTime, default=func.now())
