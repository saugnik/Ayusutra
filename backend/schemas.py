"""
Pydantic Schemas for AyurSutra Backend
Request and response models for API endpoints.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# ==================== BASE SCHEMAS ====================
class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

# ==================== USER SCHEMAS ====================
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str
    # Patient-specific fields
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    # Practitioner-specific fields
    license_number: Optional[str] = None
    specializations: Optional[List[str]] = None
    experience_years: Optional[int] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    consultation_fee: Optional[float] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseSchema):
    id: int
    email: str
    full_name: str
    role: str
    phone: Optional[str]
    profile_picture: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str
    full_name: str

# ==================== PATIENT SCHEMAS ====================
class PatientBase(BaseModel):
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []
    allergies: Optional[List[str]] = []
    prakriti_type: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientResponse(BaseSchema):
    id: int
    user_id: int
    date_of_birth: Optional[datetime]
    gender: Optional[str]
    address: Optional[str]
    emergency_contact: Optional[str]
    medical_history: List[str]
    current_medications: List[str]
    allergies: List[str]
    prakriti_type: Optional[str]
    lifestyle_preferences: Dict[str, Any]
    created_at: datetime

# ==================== PRACTITIONER SCHEMAS ====================
class PractitionerBase(BaseModel):
    license_number: Optional[str] = None
    specializations: Optional[List[str]] = []
    experience_years: Optional[int] = 0
    qualification: Optional[str] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    consultation_fee: Optional[float] = 0.0
    bio: Optional[str] = None

class PractitionerCreate(PractitionerBase):
    pass

class PractitionerUpdate(PractitionerBase):
    availability_schedule: Optional[Dict[str, Any]] = {}

class PractitionerResponse(BaseSchema):
    id: int
    user_id: int
    license_number: Optional[str]
    specializations: List[str]
    experience_years: int
    qualification: Optional[str]
    clinic_name: Optional[str]
    clinic_address: Optional[str]
    consultation_fee: float
    bio: Optional[str]
    rating: float
    total_reviews: int
    is_verified: bool
    created_at: datetime

# ==================== ADMIN SCHEMAS ====================
class AdminBase(BaseModel):
    admin_level: Optional[str] = "standard"
    permissions: Optional[List[str]] = []
    department: Optional[str] = None

class AdminCreate(AdminBase):
    pass

class AdminResponse(BaseSchema):
    id: int
    user_id: int
    admin_level: str
    permissions: List[str]
    department: Optional[str]
    created_at: datetime

# ==================== APPOINTMENT SCHEMAS ====================
class AppointmentBase(BaseModel):
    patient_id: int
    practitioner_id: int
    therapy_type: str
    scheduled_datetime: datetime
    duration_minutes: Optional[int] = 60
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    scheduled_datetime: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    patient_notes: Optional[str] = None
    practitioner_notes: Optional[str] = None

class AppointmentResponse(BaseSchema):
    id: int
    patient_id: int
    practitioner_id: int
    therapy_type: str
    scheduled_datetime: datetime
    duration_minutes: int
    status: str
    notes: Optional[str]
    patient_notes: Optional[str]
    practitioner_notes: Optional[str]
    fee: Optional[float]
    payment_status: str
    created_at: datetime
    updated_at: Optional[datetime]

# ==================== THERAPY SESSION SCHEMAS ====================
class TherapySessionBase(BaseModel):
    therapy_type: str
    pre_session_notes: Optional[str] = None
    therapy_parameters: Optional[Dict[str, Any]] = {}

class TherapySessionCreate(TherapySessionBase):
    appointment_id: int
    patient_id: int
    practitioner_id: int

class TherapySessionUpdate(BaseModel):
    status: Optional[str] = None
    session_notes: Optional[str] = None
    post_session_notes: Optional[str] = None
    vitals_before: Optional[Dict[str, Any]] = {}
    vitals_after: Optional[Dict[str, Any]] = {}
    therapy_parameters: Optional[Dict[str, Any]] = {}
    patient_feedback_during: Optional[str] = None
    complications: Optional[str] = None
    recommendations: Optional[str] = None
    next_session_recommendations: Optional[str] = None
    report: Optional[str] = None

class TherapySessionResponse(BaseSchema):
    id: int
    appointment_id: int
    patient_id: int
    practitioner_id: int
    therapy_type: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    session_notes: Optional[str]
    post_session_notes: Optional[str]
    vitals_before: Dict[str, Any]
    vitals_after: Dict[str, Any]
    therapy_parameters: Dict[str, Any]
    recommendations: Optional[str]
    report: Optional[str]
    created_at: datetime

# ==================== FEEDBACK SCHEMAS ====================
class FeedbackBase(BaseModel):
    patient_id: int
    practitioner_id: int
    appointment_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    satisfaction_level: Optional[str] = None
    comments: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(BaseSchema):
    id: int
    patient_id: int
    practitioner_id: int
    appointment_id: Optional[int]
    rating: int
    satisfaction_level: Optional[str]
    comments: Optional[str]
    therapy_effectiveness: Optional[int]
    practitioner_professionalism: Optional[int]
    facility_cleanliness: Optional[int]
    would_recommend: Optional[bool]
    suggestions: Optional[str]
    created_at: datetime

# ==================== AI ASSISTANT SCHEMAS ====================
class AIAssistantRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class AIAssistantResponse(BaseModel):
    query: str
    answer: Dict[str, Any]
    context: List[Dict[str, Any]]
    confidence: str
    sources: List[Dict[str, Any]]

# ==================== DASHBOARD SCHEMAS ====================
class DashboardStats(BaseModel):
    # Patient dashboard
    total_appointments: Optional[int] = 0
    upcoming_appointments: Optional[int] = 0
    completed_sessions: Optional[int] = 0
    active_treatments: Optional[int] = 0
    patient_satisfaction: Optional[float] = 0.0
    avg_session_duration: Optional[float] = 0.0
    
    # Practitioner dashboard
    total_patients: Optional[int] = 0
    today_appointments: Optional[int] = 0
    pending_reports: Optional[int] = 0
    success_rate: Optional[float] = 0.0
    avg_session_rating: Optional[float] = 0.0
    
    # Admin dashboard
    total_users: Optional[int] = 0
    total_practitioners: Optional[int] = 0
    recent_registrations: Optional[int] = 0
    system_health: Optional[float] = 0.0

# ==================== NOTIFICATION SCHEMAS ====================
class NotificationBase(BaseModel):
    title: str
    message: str
    type: str
    priority: Optional[str] = "normal"

class NotificationCreate(NotificationBase):
    user_id: int
    action_url: Optional[str] = None
    expires_at: Optional[datetime] = None

class NotificationResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    priority: str
    is_read: bool
    action_url: Optional[str]
    expires_at: Optional[datetime]
    created_at: datetime

# ==================== THERAPY TEMPLATE SCHEMAS ====================
class TherapyTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    duration_minutes: Optional[int] = 60
    preparation_steps: Optional[List[str]] = []
    procedure_steps: Optional[List[str]] = []
    post_care_instructions: Optional[List[str]] = []
    contraindications: Optional[List[str]] = []
    required_materials: Optional[List[str]] = []
    benefits: Optional[List[str]] = []
    suitable_conditions: Optional[List[str]] = []
    cost_range: Optional[str] = None

class TherapyTemplateCreate(TherapyTemplateBase):
    pass

class TherapyTemplateResponse(BaseSchema):
    id: int
    name: str
    description: Optional[str]
    category: str
    duration_minutes: int
    preparation_steps: List[str]
    procedure_steps: List[str]
    post_care_instructions: List[str]
    contraindications: List[str]
    required_materials: List[str]
    benefits: List[str]
    suitable_conditions: List[str]
    cost_range: Optional[str]
    is_active: bool
    created_at: datetime
