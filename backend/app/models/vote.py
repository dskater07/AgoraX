from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    vote_option = Column(String(10), nullable=False)
    ip_address = Column(String(45))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("meeting_id", "user_id", name="uq_vote_user_meeting"),)

    # Relaciones ORM
    user = relationship("User", backref="votes")
    meeting = relationship("Meeting", backref="votes")
