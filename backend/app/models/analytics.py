"""Analytics models for tracking profile views"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class ProfileView(Base):
    """Profile view tracking model"""
    __tablename__ = "profile_views"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidate_profiles.id", ondelete="CASCADE"), index=True)
    viewer_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # NULL if anonymous
    viewer_ip = Column(String(45), nullable=True)  # IPv4 or IPv6
    viewer_user_agent = Column(String(500), nullable=True)
    viewed_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    candidate_profile = relationship("CandidateProfile")
    viewer_user = relationship("User")

    class Config:
        from_attributes = True
