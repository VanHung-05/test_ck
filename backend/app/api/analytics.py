"""Analytics API routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.services.auth import AuthService
from app.services.analytics import AnalyticsService
from app.schemas.analytics import CandidateAnalytics


router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def get_current_user_id(request: Request, db: Session = Depends(get_db)):
    """Extract user_id from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    token = auth_header.replace("Bearer ", "")
    try:
        user = AuthService.get_current_user(db, token)
        return user.id
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


def get_optional_user_id(request: Request, db: Session = Depends(get_db)) -> Optional[int]:
    """Extract user_id from Authorization header (optional)"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    try:
        user = AuthService.get_current_user(db, token)
        return user.id
    except ValueError:
        return None


@router.post("/track-view/{profile_slug}")
async def track_profile_view(
    profile_slug: str,
    request: Request,
    db: Session = Depends(get_db),
    viewer_user_id: Optional[int] = Depends(get_optional_user_id)
):
    """Track a profile view (public endpoint)"""
    from app.models.candidate import CandidateProfile

    # Get candidate profile by slug
    profile = db.query(CandidateProfile).filter(
        CandidateProfile.profile_slug == profile_slug,
        CandidateProfile.is_public == True
    ).first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    # Get viewer info
    viewer_ip = request.client.host if request.client else None
    viewer_user_agent = request.headers.get("user-agent")

    # Track the view
    try:
        AnalyticsService.track_profile_view(
            db=db,
            candidate_id=profile.id,
            viewer_user_id=viewer_user_id,
            viewer_ip=viewer_ip,
            viewer_user_agent=viewer_user_agent
        )
        return {"message": "View tracked"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/my-stats", response_model=CandidateAnalytics)
async def get_my_analytics(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get analytics for current candidate"""
    try:
        analytics = AnalyticsService.get_candidate_analytics(db, user_id)
        return analytics
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
