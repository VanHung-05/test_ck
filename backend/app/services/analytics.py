"""Analytics service for tracking and reporting"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional
from app.models.analytics import ProfileView
from app.models.candidate import CandidateProfile
from app.models.recruiter import JobInvitation
from app.schemas.analytics import CandidateAnalytics


class AnalyticsService:
    """Service for analytics operations"""

    @staticmethod
    def track_profile_view(
        db: Session,
        candidate_id: int,
        viewer_user_id: Optional[int] = None,
        viewer_ip: Optional[str] = None,
        viewer_user_agent: Optional[str] = None
    ) -> ProfileView:
        """Track a profile view"""
        view = ProfileView(
            candidate_id=candidate_id,
            viewer_user_id=viewer_user_id,
            viewer_ip=viewer_ip,
            viewer_user_agent=viewer_user_agent
        )
        db.add(view)
        db.commit()
        db.refresh(view)
        return view

    @staticmethod
    def get_candidate_analytics(db: Session, user_id: int) -> CandidateAnalytics:
        """Get analytics summary for a candidate"""
        # Get candidate profile
        profile = db.query(CandidateProfile).filter(
            CandidateProfile.user_id == user_id
        ).first()

        if not profile:
            raise ValueError("Profile not found")

        # Total views
        total_views = db.query(func.count(ProfileView.id)).filter(
            ProfileView.candidate_id == profile.id
        ).scalar() or 0

        # Recent views (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_views = db.query(func.count(ProfileView.id)).filter(
            ProfileView.candidate_id == profile.id,
            ProfileView.viewed_at >= thirty_days_ago
        ).scalar() or 0

        # Total invitations
        total_invitations = db.query(func.count(JobInvitation.id)).filter(
            JobInvitation.candidate_id == profile.id
        ).scalar() or 0

        # Recent invitations (last 30 days)
        recent_invitations = db.query(func.count(JobInvitation.id)).filter(
            JobInvitation.candidate_id == profile.id,
            JobInvitation.created_at >= thirty_days_ago
        ).scalar() or 0

        return CandidateAnalytics(
            total_views=total_views,
            total_invitations=total_invitations,
            recent_views=recent_views,
            recent_invitations=recent_invitations
        )
