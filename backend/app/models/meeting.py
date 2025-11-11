from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    quorum_min = Column(Float, default=51.0)
    status = Column(String(20), default="pendiente")  # pendiente, abierta, cerrada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    opened_at = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
