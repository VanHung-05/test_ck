"""Analytics schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProfileViewCreate(BaseModel):
    """Schema for creating a profile view record"""
    candidate_id: int
    viewer_user_id: Optional[int] = None
    viewer_ip: Optional[str] = None
    viewer_user_agent: Optional[str] = None


class ProfileViewResponse(BaseModel):
    """Schema for profile view response"""
    id: int
    candidate_id: int
    viewer_user_id: Optional[int]
    viewed_at: datetime

    class Config:
        from_attributes = True


class CandidateAnalytics(BaseModel):
    """Schema for candidate analytics summary"""
    total_views: int
    total_invitations: int
    recent_views: int  # Last 30 days
    recent_invitations: int  # Last 30 days
