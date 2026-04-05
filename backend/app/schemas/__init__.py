"""Schemas package"""
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.candidate import (
    CandidateProfileResponse, CandidateProfileUpdate, SkillCreate, SkillResponse, SkillUpdate,
    ExperienceCreate, ExperienceResponse, ExperienceUpdate, ProjectCreate, ProjectResponse, ProjectUpdate,
    CVResponse
)
from app.schemas.recruiter import (
    CompanyRegister, CompanyUpdate, CompanyResponse, JobInvitationCreate,
    JobInvitationResponse, CandidateSearchResult
)
from app.schemas.analytics import ProfileViewCreate, ProfileViewResponse, CandidateAnalytics
