"""
Pydantic Schemas for AyurSutra Backend
Request and response models for API endpoints.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

class UserShort(BaseModel):
    full_name: str
    email: EmailStr
    profile_picture: Optional[str] = None
    
    class Config:
        orm_mode = True

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

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    profile_picture: Optional[str] = None
    
    class Config:
        orm_mode = True

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

class AvailabilitySlot(BaseModel):
    start_time: str
    end_time: str
    location: Optional[str] = "Main Clinic"

class AvailabilitySchedule(BaseModel):
    monday: List[AvailabilitySlot] = []
    tuesday: List[AvailabilitySlot] = []
    wednesday: List[AvailabilitySlot] = []
    thursday: List[AvailabilitySlot] = []
    friday: List[AvailabilitySlot] = []
    saturday: List[AvailabilitySlot] = []
    sunday: List[AvailabilitySlot] = []

class PractitionerBase(BaseModel):
    license_number: str
    specializations: List[str] = []
    experience_years: int = 0
    qualification: Optional[str] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    consultation_fee: float = 0.0
    availability_schedule: Dict[str, Any] = {} # Can strictly use AvailabilitySchedule but Dict is safer for DB JSON compatibility initially
    bio: Optional[str] = None

class PractitionerCreate(PractitionerBase):
    pass

class PractitionerUpdate(BaseModel):
    specializations: Optional[List[str]] = None
    experience_years: Optional[int] = None
    qualification: Optional[str] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    consultation_fee: Optional[float] = None
    availability_schedule: Optional[AvailabilitySchedule] = None # Updated to be consistent
    bio: Optional[str] = None

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
    availability_schedule: AvailabilitySchedule
    bio: Optional[str]
    rating: float
    total_reviews: int
    is_verified: bool
    user: Optional['UserShort'] = None
    created_at: datetime

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

class AIAssistantRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class AIAssistantResponse(BaseModel):
    query: str
    answer: Dict[str, Any]
    context: List[Dict[str, Any]]
    confidence: str
    sources: List[Dict[str, Any]]

class DashboardStats(BaseModel):
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

class PatientListItem(BaseModel):
    id: int
    name: str
    age: Optional[int]
    gender: Optional[str]
    phone: Optional[str]
    email: str
    current_therapy: Optional[str] = "None"
    stage: Optional[str] = "N/A"
    next_appointment: Optional[datetime] = None
    status: str = "active"
    prakriti: Optional[str] = "Unknown"

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

# ==================== HEALTH LOG SCHEMAS ====================
class HealthLogBase(BaseModel):
    dosha_vata: Optional[int] = 50
    dosha_pitta: Optional[int] = 50
    dosha_kapha: Optional[int] = 50
    sleep_score: Optional[int] = None
    stress_level: Optional[str] = "Medium"
    hydration: Optional[float] = 0.0
    weight: Optional[float] = None
    blood_pressure: Optional[str] = None
    notes: Optional[str] = None
    recommendations: Optional[str] = None

class HealthLogCreate(HealthLogBase):
    patient_id: int

class HealthLogResponse(HealthLogBase):
    id: int
    patient_id: int
    practitioner_id: int
    date: datetime
    created_at: datetime
    
    class Config:
        orm_mode = True


# ==================== HEALTH SUPPORT SCHEMAS ====================
class SymptomCreate(BaseModel):
    symptom_name: str
    severity: str  # low, moderate, high, severe
    notes: Optional[str] = None
    duration_days: Optional[int] = None

class SymptomResponse(BaseSchema):
    id: int
    patient_id: int
    symptom_name: str
    severity: str
    notes: Optional[str] = None
    duration_days: Optional[int] = None
    created_at: datetime

class AIHealthRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None

class AIHealthResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    conversation_id: str

class HealthRecommendation(BaseModel):
    category: str  # diet, lifestyle, herbs, therapy
    suggestion: str
    reason: str
    priority: Optional[str] = "normal"  # low, normal, high

class HealthRecommendationsResponse(BaseModel):
    recommendations: List[HealthRecommendation]
    dosha_analysis: Optional[Dict[str, Any]] = None

# ==================== CHAT SUPPORT SCHEMAS ====================
class ChatMessageCreate(BaseModel):
    recipient_id: int
    recipient_type: str  # patient or practitioner
    content: str

class ChatMessageResponse(BaseSchema):
    id: int
    sender_id: int
    sender_type: str
    recipient_id: int
    recipient_type: str
    content: str
    read: bool
    created_at: datetime

class PractitionerAvailability(BaseModel):
    id: int
    name: str
    specialization: Optional[str] = None
    online: bool
    last_seen: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class AIChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class AIChatResponse(BaseModel):
    reply: str
    conversation_id: str


# ==================== PATIENT REPORT SCHEMAS ====================
class ReportHealthStats(BaseModel):
    average_sleep: Optional[float] = 0.0
    average_hydration: Optional[float] = 0.0
    stress_trend: Optional[str] = "Stable"
    dominant_dosha: Optional[str] = "Mixed"

class PatientReportResponse(BaseModel):
    generated_at: datetime
    patient_name: str
    patient_age: Optional[int]
    patient_gender: Optional[str]
    prakriti_type: Optional[str]
    
    # Sections
    health_stats: ReportHealthStats
    recent_appointments: List[AppointmentResponse]
    recent_health_logs: List[HealthLogResponse]
    recent_symptoms: List[SymptomResponse]
    doctor_notes: Optional[str] = None

class TreatmentTypeStat(BaseModel):
    type: str
    count: int
    success_rate: float

class TreatmentAnalyticsResponse(BaseModel):
    total_treatments: int
    success_rate_overall: float
    type_distribution: List[TreatmentTypeStat]
    monthly_trends: List[Dict[str, Any]] # e.g., [{"month": "Jan", "count": 10}]

class MonthlySummaryResponse(BaseModel):
    month: str
    total_revenue: float
    total_appointments: int
    new_patients: int
    popular_therapies: List[str]
    appointment_status_counts: Dict[str, int]

class FeedbackSummary(BaseModel):
    average_rating: float
    total_reviews: int
    rating_distribution: Dict[int, int] # 5 stars: 10, 4 stars: 5...
    recent_feedback: List[FeedbackResponse]

class FeedbackReportResponse(BaseModel):
    summary: FeedbackSummary
    improvement_areas: List[str]
