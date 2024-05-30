from enum import Enum

from sqlalchemy import ForeignKey, Integer, Column, String, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class ItemStatus(str, Enum):
    pending = "pending"
    done = "done"
    in_progress = "in_progress"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, index=True, default=ItemStatus.pending)
    due_date = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")
