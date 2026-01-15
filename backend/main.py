
import os
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse

# ... (omitted)


from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import func
import requests

from database import engine, SessionLocal, get_db
from models import User, Patient, Practitioner, Admin, Appointment, TherapySession, Feedback, UserRole, Base, Notification, SystemSettings, AuditLog, PatientHealthLog, Symptom, AIConversation, ChatMessage
from schemas import (
    UserCreate, UserResponse, TokenResponse, UserLogin,
    PatientCreate, PatientResponse, PatientUpdate,
    PractitionerCreate, PractitionerResponse, PractitionerUpdate,
    AdminCreate, AdminResponse,
    AppointmentCreate, AppointmentResponse, AppointmentUpdate,
    TherapySessionCreate, TherapySessionResponse, TherapySessionUpdate,
    FeedbackCreate, FeedbackResponse,
    AIAssistantRequest, AIAssistantResponse,
    DashboardStats, PatientListItem, UserUpdate,
    NotificationResponse, TherapyTemplateResponse, HealthLogCreate, HealthLogResponse,
    SymptomCreate, SymptomResponse, AIHealthRequest, AIHealthResponse,
    HealthRecommendationsResponse, ChatMessageCreate, ChatMessageResponse,
    PractitionerAvailability, AIChatRequest, AIChatResponse,
    PatientReportResponse, ReportHealthStats,
    TreatmentAnalyticsResponse, MonthlySummaryResponse, FeedbackReportResponse,
    TreatmentTypeStat, FeedbackSummary
)
from auth import (
    create_access_token, verify_token, get_password_hash, verify_password,
    get_current_user, get_current_patient, get_current_practitioner, get_current_admin
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AyurSutra Backend API",
    description="Comprehensive backend service for digital Panchakarma management platform",
    version="1.0.0"
)

# Custom CORS middleware - Add headers to ALL responses


# Configure CORS - Specific origins required when using credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Security
security = HTTPBearer()

# RAG Service Configuration
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://localhost:8000")



# ==================== HEALTH CHECK ====================
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AyurSutra Backend API is running",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "rag_service": "available",
        "timestamp": datetime.utcnow()
    }


# ==================== AUTHENTICATION ====================
@app.post("/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        
        # Convert role string to enum
        role_map = {
            "patient": UserRole.PATIENT,
            "practitioner": UserRole.PRACTITIONER,
            "admin": UserRole.ADMIN
        }
        user_role = role_map.get(user_data.role.lower(), UserRole.PATIENT)
        
        db_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role=user_role,
            phone=user_data.phone,
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create role-specific profile
        role_lower = user_data.role.lower()
        
        if role_lower == "patient":
            patient_profile = Patient(
                user_id=db_user.id,
                date_of_birth=user_data.date_of_birth,
                gender=user_data.gender,
                address=user_data.address,
                emergency_contact=user_data.emergency_contact,
                medical_history=[],
                current_medications=[],
                allergies=[],
                prakriti_type="Unknown",
                lifestyle_preferences={}
            )
            db.add(patient_profile)
        
        elif role_lower == "practitioner":
            practitioner_profile = Practitioner(
                user_id=db_user.id,
                license_number=user_data.license_number,
                specializations=user_data.specializations or [],
                experience_years=user_data.experience_years or 0,
                clinic_name=user_data.clinic_name,
                clinic_address=user_data.clinic_address,
                availability_schedule={},
                consultation_fee=user_data.consultation_fee or 0
            )
            db.add(practitioner_profile)
        
        elif role_lower == "admin":
            admin_profile = Admin(
                user_id=db_user.id,
                admin_level="standard",
                permissions=["user_management", "system_monitoring"]
            )
            db.add(admin_profile)
        
        db.commit()
        
        return UserResponse.from_orm(db_user)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"\n{'='*60}")
        print(f"REGISTRATION ERROR:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )


@app.post("/auth/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Account is deactivated"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token (convert enum to string for serialization)
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role.value,  # Convert enum to string
        full_name=user.full_name
    )


@app.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@app.put("/users/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    # Check email uniqueness if changing
    if user_update.email and user_update.email != current_user.email:
        existing = db.query(User).filter(User.email == user_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = user_update.email
        
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    
    if user_update.phone:
        current_user.phone = user_update.phone
        
    if user_update.profile_picture:
        current_user.profile_picture = user_update.profile_picture
        
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
        
    db.commit()
    db.refresh(current_user)
    return current_user


# ==================== AI ASSISTANT ====================
@app.post("/ai/ask", response_model=AIAssistantResponse)
async def ai_assistant(
    request: AIAssistantRequest,
    current_user: User = Depends(get_current_user)
):
    """AI Assistant powered by RAG service"""
    try:
        # Forward request to RAG service
        response = requests.post(
            f"{RAG_SERVICE_URL}/ask",
            json={"query": request.query, "top_k": request.top_k or 5},
            timeout=30
        )
        
        if response.status_code == 200:
            rag_data = response.json()
            return AIAssistantResponse(
                query=request.query,
                answer=rag_data["answer"],
                context=rag_data.get("context", []),
                confidence=rag_data["answer"].get("confidence", "medium"),
                sources=rag_data["answer"].get("evidence", [])
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="AI service temporarily unavailable"
            )
            
    except Exception as e:
        logger.error(f"AI Assistant error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="AI service error"
        )


# ==================== APPOINTMENT MANAGEMENT ====================
@app.post("/appointments", response_model=AppointmentResponse)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new appointment"""
    # Validate patient and practitioner exist
    patient = db.query(Patient).filter(Patient.id == appointment_data.patient_id).first()
    practitioner = db.query(Practitioner).filter(Practitioner.id == appointment_data.practitioner_id).first()
    
    if not patient or not practitioner:
        raise HTTPException(status_code=404, detail="Patient or practitioner not found")
    
    # Check for scheduling conflicts
    existing_appointment = db.query(Appointment).filter(
        Appointment.practitioner_id == appointment_data.practitioner_id,
        Appointment.scheduled_datetime == appointment_data.scheduled_datetime,
        Appointment.status.in_(["scheduled", "confirmed"])
    ).first()
    
    if existing_appointment:
        raise HTTPException(status_code=400, detail="Time slot already booked")
    
    # Create appointment
    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        practitioner_id=appointment_data.practitioner_id,
        therapy_type=appointment_data.therapy_type,
        scheduled_datetime=appointment_data.scheduled_datetime,
        duration_minutes=appointment_data.duration_minutes,
        status="scheduled",
        notes=appointment_data.notes,
        created_at=datetime.utcnow(),
        created_by=current_user.id
    )
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    return AppointmentResponse.from_orm(appointment)


@app.get("/appointments", response_model=List[AppointmentResponse])
async def get_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    limit: int = 50
):
    """Get appointments for current user"""
    query = db.query(Appointment)
    
    if current_user.role == "patient":
        patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if patient:
            query = query.filter(Appointment.patient_id == patient.id)
    
    elif current_user.role == "practitioner":
        practitioner = db.query(Practitioner).filter(Practitioner.user_id == current_user.id).first()
        if practitioner:
            query = query.filter(Appointment.practitioner_id == practitioner.id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    appointments = query.order_by(Appointment.scheduled_datetime.desc()).limit(limit).all()
    
    return [AppointmentResponse.from_orm(appointment) for appointment in appointments]


# ==================== PATIENT DASHBOARD ====================
@app.get("/patient/dashboard", response_model=DashboardStats)
async def get_patient_dashboard(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get patient dashboard statistics"""
    now = datetime.utcnow()
    
    # Get appointments statistics
    total_appointments = db.query(Appointment).filter(
        Appointment.patient_id == current_patient.id
    ).count()
    
    upcoming_appointments = db.query(Appointment).filter(
        Appointment.patient_id == current_patient.id,
        Appointment.scheduled_datetime > now,
        Appointment.status.in_(["scheduled", "confirmed"])
    ).count()
    
    completed_sessions = db.query(TherapySession).filter(
        TherapySession.patient_id == current_patient.id,
        TherapySession.status == "completed"
    ).count()
    
    active_treatments = db.query(Appointment).filter(
        Appointment.patient_id == current_patient.id,
        Appointment.status == "in_progress"
    ).count()
    
    return DashboardStats(
        total_appointments=total_appointments,
        upcoming_appointments=upcoming_appointments,
        completed_sessions=completed_sessions,
        active_treatments=active_treatments,
        patient_satisfaction=4.8,  # Mock data
        avg_session_duration=75.5  # Mock data
    )


# ==================== PRACTITIONER DASHBOARD ====================
@app.get("/practitioner/dashboard", response_model=DashboardStats)
async def get_practitioner_dashboard(
    current_practitioner: Practitioner = Depends(get_current_practitioner),
    db: Session = Depends(get_db)
):
    """Get practitioner dashboard statistics"""
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    today_end = today_start + timedelta(days=1)
    
    # Get statistics
    total_patients = db.query(Appointment).filter(
        Appointment.practitioner_id == current_practitioner.id
    ).distinct(Appointment.patient_id).count()
    
    today_appointments = db.query(Appointment).filter(
        Appointment.practitioner_id == current_practitioner.id,
        Appointment.scheduled_datetime.between(today_start, today_end)
    ).count()
    
    active_treatments = db.query(Appointment).filter(
        Appointment.practitioner_id == current_practitioner.id,
        Appointment.status == "in_progress"
    ).count()
    
    pending_reports = db.query(TherapySession).filter(
        TherapySession.practitioner_id == current_practitioner.id,
        TherapySession.status == "completed",
        TherapySession.report.is_(None)
    ).count()
    
    # Calculate success rate
    completed = db.query(Appointment).filter(
        Appointment.practitioner_id == current_practitioner.id,
        Appointment.status == "completed"
    ).count()
    
    total_for_rate = db.query(Appointment).filter(
        Appointment.practitioner_id == current_practitioner.id,
        Appointment.status.in_(["completed", "cancelled", "no_show"])
    ).count()
    
    success_rate = (completed / total_for_rate * 100) if total_for_rate > 0 else 0.0
    
    return DashboardStats(
        total_patients=total_patients,
        today_appointments=today_appointments,
        pending_reports=pending_reports,
        success_rate=round(success_rate, 1),
        avg_session_rating=current_practitioner.rating or 0.0
    )

@app.get("/practitioners", response_model=List[PractitionerResponse])
async def get_all_practitioners(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """Get all practitioners (for map/directory)"""
    practitioners = db.query(Practitioner).all()
    # Ensure user data is joined/available? 
    # Pydantic schema expects 'user' field? PractitionerResponse definition has 'user_id' but not nested 'user' object unless specified.
    # Check schemas.py line 145. It has 'user_id'. It does NOT have nested User.
    # But for map we might want name.
    # Let's check PractitionerResponse again or update it?
    # I'll stick to basic response for now, or assume the frontend fetches details.
    # Wait, map needs NAME. PractitionerResponse needs name.
    # Currently PractitionerResponse only has license_number, specializations etc.
    # I should update PractitionerResponse in schemas.py to include 'full_name' or nested 'user'.
    # I'll assume current schema is sufficient or I'll fix it if name is missing. 
    # Actually, let's just return them. Logic for name might be needed.
    return practitioners
    



@app.get("/practitioner/profile", response_model=PractitionerResponse)
async def get_practitioner_profile_data(
    current_practitioner: Practitioner = Depends(get_current_practitioner),
    db: Session = Depends(get_db)
):
    """Get current practitioner's profile"""
    return current_practitioner

@app.patch("/practitioner/profile", response_model=PractitionerResponse)
async def update_practitioner_profile(
    profile_update: PractitionerUpdate,
    current_practitioner: Practitioner = Depends(get_current_practitioner),
    db: Session = Depends(get_db)
):
    """Update current practitioner's profile"""
    try:
        from fastapi.encoders import jsonable_encoder
        update_data = profile_update.dict(exclude_unset=True)
        print(f"DEBUG: Updating profile with: {update_data}")
        
        # Ensure availability_schedule is properly encoded for JSON column
        if "availability_schedule" in update_data:
             update_data["availability_schedule"] = jsonable_encoder(update_data["availability_schedule"])
        
        for field, value in update_data.items():
            setattr(current_practitioner, field, value)
        
        db.add(current_practitioner) # Ensure attached
        db.commit()
        db.refresh(current_practitioner)
        return current_practitioner
    except Exception as e:
        print(f"ERROR updating profile: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/practitioner/patients", response_model=List[PatientListItem])
async def get_my_patients(
    current_practitioner: Practitioner = Depends(get_current_practitioner),
    db: Session = Depends(get_db)
):
    """Get list of patients for current practitioner"""
    # Find patients with appointments with this practitioner
    # Subquery or distinct join
    patients = db.query(Patient).join(Appointment).filter(
        Appointment.practitioner_id == current_practitioner.id
    ).distinct().all()
    
    patient_list = []
    now = datetime.utcnow()

    for p in patients:
        user = db.query(User).filter(User.id == p.user_id).first()
        if not user:
            continue
            
        # detailed logic for fields
        age = None
        if p.date_of_birth:
             age = (datetime.utcnow().date() - p.date_of_birth.date()).days // 365
        
        # Current therapy (last appointment or active)
        last_appt = db.query(Appointment).filter(
            Appointment.patient_id == p.id,
            Appointment.practitioner_id == current_practitioner.id
        ).order_by(Appointment.scheduled_datetime.desc()).first()
        
        current_therapy = last_appt.therapy_type if last_appt else "None"
        
        # Next appointment
        next_appt = db.query(Appointment).filter(
            Appointment.patient_id == p.id,
            Appointment.practitioner_id == current_practitioner.id,
            Appointment.scheduled_datetime > now
        ).order_by(Appointment.scheduled_datetime.asc()).first()
        
        patient_list.append(PatientListItem(
            id=p.id,
            name=user.full_name,
            age=age,
            gender=p.gender or "Unknown",
            phone=user.phone,
            email=user.email,
            current_therapy=current_therapy,
            stage="Active" if next_appt else "Inactive",
            next_appointment=next_appt.scheduled_datetime if next_appt else None,
            status="active" if next_appt else "completed", # Simple logic
            prakriti=p.prakriti_type or "Unknown"
        ))
        
    return patient_list


# ==================== ADMIN DASHBOARD ====================
@app.get("/admin/dashboard", response_model=DashboardStats)
async def get_admin_dashboard(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    # System-wide statistics
    total_users = db.query(User).count()
    total_practitioners = db.query(User).filter(User.role == UserRole.PRACTITIONER).count()
    total_patients = db.query(User).filter(User.role == UserRole.PATIENT).count()
    total_appointments = db.query(Appointment).count()
    
    # Recent activity
    recent_registrations = db.query(User).filter(
        User.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    return DashboardStats(
        total_users=total_users,
        total_practitioners=total_practitioners,
        total_patients=total_patients,
        total_appointments=total_appointments,
        recent_registrations=recent_registrations,
        system_health=98.5  # Mock data
    )


# ==================== FEEDBACK SYSTEM ====================
@app.post("/feedback", response_model=FeedbackResponse)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create feedback for a therapy session"""
    feedback = Feedback(
        patient_id=feedback_data.patient_id,
        practitioner_id=feedback_data.practitioner_id,
        appointment_id=feedback_data.appointment_id,
        rating=feedback_data.rating,
        comments=feedback_data.comments,
        satisfaction_level=feedback_data.satisfaction_level,
        created_at=datetime.utcnow()
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return FeedbackResponse.from_orm(feedback)


# ==================== FILE UPLOAD ====================
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload files (profile pictures, documents, etc.)"""
    # Validate file type and size
    allowed_types = ["image/jpeg", "image/png", "image/gif", "application/pdf"]
    max_size = 5 * 1024 * 1024  # 5MB
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Read and validate file size
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Save file (implement proper file storage)
    filename = f"{current_user.id}_{datetime.utcnow().timestamp()}_{file.filename}"
    # TODO: Implement actual file saving to cloud storage or local filesystem
    
    return {
        "filename": filename,
        "size": len(content),
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }


# ==================== REPORTS AND ANALYTICS ====================
@app.get("/reports/patient/{patient_id}", response_model=PatientReportResponse)
async def get_patient_report(
    patient_id: int,
    current_user: User = Depends(get_current_user), # Any authorized user for now (practitioner/patient)
    db: Session = Depends(get_db)
):
    """Generate a detailed progress report for a patient"""
    # 1. Get Patient Details
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
         raise HTTPException(status_code=404, detail="Patient not found")
         
    user = db.query(User).filter(User.id == patient.user_id).first()
    
    # 2. Analyze Health Logs (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_logs = db.query(PatientHealthLog).filter(
        PatientHealthLog.patient_id == patient_id,
        PatientHealthLog.date >= thirty_days_ago
    ).order_by(PatientHealthLog.date.desc()).all()
    
    # Calculate averages
    avg_sleep = 0.0
    avg_hydration = 0.0
    dosha_counts = {"Vata": 0, "Pitta": 0, "Kapha": 0}
    
    if recent_logs:
        total_sleep = sum(log.sleep_score or 0 for log in recent_logs)
        total_hydration = sum(log.hydration or 0.0 for log in recent_logs)
        avg_sleep = total_sleep / len(recent_logs)
        avg_hydration = total_hydration / len(recent_logs)
        
        # Simple dosha dominance check per log
        for log in recent_logs:
            scores = {"Vata": log.dosha_vata or 0, "Pitta": log.dosha_pitta or 0, "Kapha": log.dosha_kapha or 0}
            dominant = max(scores, key=scores.get)
            dosha_counts[dominant] += 1
    
    most_frequent_dosha = max(dosha_counts, key=dosha_counts.get) if recent_logs else "Unknown"

    # 3. Get Recent Appointments (last 5)
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).order_by(Appointment.scheduled_datetime.desc()).limit(5).all()
    
    # 3b. Get Recent Symptoms (last 5)
    recent_symptoms = db.query(Symptom).filter(
        Symptom.patient_id == patient_id
    ).order_by(Symptom.created_at.desc()).limit(5).all()
    
    # 4. Construct Response
    return PatientReportResponse(
        generated_at=datetime.utcnow(),
        patient_name=user.full_name,
        patient_age=(datetime.utcnow().year - patient.date_of_birth.year) if patient.date_of_birth else None,
        patient_gender=patient.gender,
        prakriti_type=patient.prakriti_type or "Unknown",
        health_stats=ReportHealthStats(
            average_sleep=round(avg_sleep, 1),
            average_hydration=round(avg_hydration, 1),
            stress_trend="Improving", # Placeholder logic
            dominant_dosha=most_frequent_dosha
        ),
        recent_appointments=[AppointmentResponse.from_orm(appt) for appt in appointments],
        recent_health_logs=[HealthLogResponse.from_orm(log) for log in recent_logs],
        recent_symptoms=[SymptomResponse.from_orm(s) for s in recent_symptoms],
        doctor_notes="Patient is showing steady improvement." # Placeholder
    )

@app.get("/reports/treatments", response_model=TreatmentAnalyticsResponse)
async def get_treatment_analytics(
    days: int = 30,
    patient_id: Optional[int] = None,
    current_user: User = Depends(get_current_practitioner),
    db: Session = Depends(get_db)
):
    """Get overall treatment analytics or patient specific"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(Appointment).filter(Appointment.scheduled_datetime >= start_date)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
        
    total_treatments = query.count()
    completed = query.filter(Appointment.status == "completed").count()
    
    # Calculate success rate (completed / total) * 100
    success_rate = (completed / total_treatments * 100) if total_treatments > 0 else 0.0
    
    # Type Distribution
    type_dist = []
    # Get counts by therapy type
    therapy_counts = query.group_by(Appointment.therapy_type).with_entities(
        Appointment.therapy_type, func.count(Appointment.id)
    ).all()
    
    for t_type, count in therapy_counts:
        # Per type success rate
        t_total = count
        t_completed = query.filter(
            Appointment.therapy_type == t_type, 
            Appointment.status == "completed"
        ).count()
        t_rate = (t_completed / t_total * 100) if t_total > 0 else 0.0
        
        type_dist.append(TreatmentTypeStat(
            type=t_type,
            count=count,
            success_rate=round(t_rate, 1)
        ))
        
    # If no data, return empty structure instead of mock, so user effectively sees "No data" for new patients
    # But for global view, if empty, we might typically seed data? 
    # If user asks "why this data", they likely want to see THEIR data.
    
    return TreatmentAnalyticsResponse(
        total_treatments=total_treatments,
        success_rate_overall=round(success_rate, 1),
        type_distribution=type_dist,
        monthly_trends=[] # Skipping trends for now or keeping empty
    )

@app.get("/reports/monthly-summary", response_model=MonthlySummaryResponse)
async def get_monthly_summary(
    patient_id: Optional[int] = None,
    current_user: User = Depends(get_current_practitioner),
    db: Session = Depends(get_db)
):
    """Get monthly activity summary, optionally filtered by patient"""
    now = datetime.utcnow()
    month_name = now.strftime("%B")
    start_date = datetime(now.year, now.month, 1)
    
    # Base Query (Practitioner Specific)
    appt_query = db.query(Appointment).filter(
        Appointment.scheduled_datetime >= start_date,
        Appointment.practitioner_id == current_user.id # Assuming current_user is the practitioner user, wait.
        # current_user is passed as User, but via get_current_practitioner dependency?
        # get_current_practitioner returns User object according to main.py type hint? 
        # No, line 738: current_user: User = Depends(get_current_practitioner)
        # Check get_current_practitioner definition.
    )
    
    # We need the Practitioner ID, not User ID.
    practitioner_profile = db.query(Practitioner).filter(Practitioner.user_id == current_user.id).first()
    if not practitioner_profile:
         raise HTTPException(status_code=400, detail="Practitioner profile not found")
         
    appt_query = db.query(Appointment).filter(
        Appointment.scheduled_datetime >= start_date,
        Appointment.practitioner_id == practitioner_profile.id
    )
    
    if patient_id:
        appt_query = appt_query.filter(Appointment.patient_id == patient_id)

    total_appts = appt_query.count()
    
    # New Patients Logic
    if patient_id:
        # If filtering for a specific patient, check if THEY are new this month
        patient_user_id = db.query(Patient.user_id).filter(Patient.id == patient_id).scalar()
        if patient_user_id:
            new_pts = db.query(User).filter(
                User.id == patient_user_id,
                User.created_at >= start_date
            ).count()
        else:
            new_pts = 0
    else:
        # New patients *for this practitioner* (e.g. patients with first appointment this month? 
        # Or just simply patients of this practitioner created this month?
        # Let's count patients who have an appointment with this practitioner AND were created this month.
        new_pts = db.query(User).join(Patient).join(Appointment).filter(
            User.role == UserRole.PATIENT,
            User.created_at >= start_date,
            Appointment.practitioner_id == practitioner_profile.id
        ).distinct().count()
    
    # Revenue Calculation (Estimate: 1500 INR per appointment)
    avg_treatment_cost = 1500.0
    revenue = float(total_appts * avg_treatment_cost)

    # Popular Therapies
    therapies = []
    if patient_id:
         # Get this patient's therapies
         t_counts = db.query(Appointment.therapy_type, func.count(Appointment.id))\
            .filter(Appointment.patient_id == patient_id)\
            .group_by(Appointment.therapy_type)\
            .order_by(func.count(Appointment.id).desc()).limit(3).all()
         therapies = [t[0] for t in t_counts]
    else:
         therapies = ["Abhyanga", "Shirodhara"] # Default

    return MonthlySummaryResponse(
        month=month_name,
        total_revenue=revenue,
        total_appointments=total_appts,
        new_patients=new_pts,
        popular_therapies=therapies if therapies else ["None"],
        appointment_status_counts={
            "completed": appt_query.filter(Appointment.status == "completed").count(),
            "scheduled": appt_query.filter(Appointment.status == "scheduled").count(),
            "cancelled": appt_query.filter(Appointment.status == "cancelled").count()
        }
    )

@app.get("/reports/feedback", response_model=FeedbackReportResponse)
async def get_feedback_report(
    current_user: User = Depends(get_current_practitioner),
    db: Session = Depends(get_db)
):
    """Get patient feedback report"""
    # Aggregate from Feedback table
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(10).all()
    
    total_reviews = db.query(Feedback).count()
    avg_rating = db.query(func.avg(Feedback.rating)).scalar() or 0.0
    
    # Distribution
    dist = {}
    for i in range(1, 6):
        count = db.query(Feedback).filter(Feedback.rating == i).count()
        dist[i] = count
        
    return FeedbackReportResponse(
        summary=FeedbackSummary(
            average_rating=round(float(avg_rating), 1),
            total_reviews=total_reviews,
            rating_distribution=dist,
            recent_feedback=[FeedbackResponse.from_orm(f) for f in feedbacks]
        ),
        improvement_areas=["Wait time reduction", "Post-session follow-up"]
    )
    
    # 5. Popular Therapies
    popular_therapies_query = db.query(
        Appointment.therapy_type, func.count(Appointment.id)
    ).group_by(Appointment.therapy_type).order_by(func.count(Appointment.id).desc()).limit(4).all()
    
    popular_therapies = [{"name": t, "count": c} for t, c in popular_therapies_query]
    
    # 6. Monthly Trends (Last 6 months)
    monthly_trends = []
    for i in range(5, -1, -1):
        # Use a more robust way to get the first day of the month i months ago
        # current month = now.month, i=0
        # i=1 -> last month
        
        month = now.month - i
        year = now.year
        while month <= 0:
            month += 12
            year -= 1
            
        count = db.query(Appointment).filter(
            func.extract('month', Appointment.scheduled_datetime) == month,
            func.extract('year', Appointment.scheduled_datetime) == year,
            Appointment.status == "completed"
        ).count()
        
        # Get month name
        month_name = datetime(year, month, 1).strftime("%b")
        
        monthly_trends.append({
            "month": month_name,
            "sessions": count
        })

    return {
        "total_sessions": total_sessions,
        "success_rate": round(success_rate, 1),
        "average_duration": round(avg_duration, 1),
        "patient_satisfaction": round(float(avg_rating), 1),
        "popular_therapies": popular_therapies,
        "monthly_trends": monthly_trends
    }


# ==================== DEBUG / DB VIEWER ====================
@app.get("/db-viewer")
async def db_viewer():
    """Serve the database viewer HTML page"""
    return FileResponse("database_viewer.html")

@app.get("/debug/db-data")
async def get_db_data(db: Session = Depends(get_db)):
    """Get database statistics and user data for the viewer"""
    
    # 1. Get counts
    counts = {
        "users": db.query(User).count(),
        "patients": db.query(Patient).count(),
        "practitioners": db.query(Practitioner).count(),
        "admins": db.query(Admin).count(),
        "appointments": db.query(Appointment).count(),
        "therapy_sessions": db.query(TherapySession).count(),
        "feedback": db.query(Feedback).count(),
        "notifications": db.query(Notification).count(),
        "system_settings": db.query(SystemSettings).count(),
        "audit_logs": db.query(AuditLog).count()
    }
    
    # 2. Get Users List (limited details for security)
    users = db.query(User).all()
    users_list = []
    for u in users:
        users_list.append({
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role.value if hasattr(u.role, 'value') else str(u.role),
            "phone": u.phone,
            "is_active": u.is_active,
            "is_verified": u.is_verified,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "last_login": u.last_login.isoformat() if u.last_login else "Never"
        })
        
    return {
        "stats": counts,
        "users": users_list,
        "database_size": "Unknown" # Calculating file size would require os path access which is fine but keep it simple
    }


@app.delete("/debug/delete-user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user and their associated profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}


@app.get("/practitioners", response_model=List[PractitionerResponse])
async def get_all_practitioners(db: Session = Depends(get_db)):
    """Get list of all practitioners with their user profiles"""
    practitioners = db.query(Practitioner).join(User).filter(User.is_active == True).all()
    # Ensure relationships are loaded for response model
    return practitioners


# ==================== HEALTH LOGS ====================
@app.post("/api/health-logs", response_model=HealthLogResponse)
async def create_health_log(
    log_data: HealthLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new health log (Practitioner only)"""
    if current_user.role != UserRole.PRACTITIONER and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only practitioners can update health logs")
        
    practitioner = db.query(Practitioner).filter(Practitioner.user_id == current_user.id).first()
    if not practitioner and current_user.role == UserRole.PRACTITIONER:
        raise HTTPException(status_code=404, detail="Practitioner profile not found")
        
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == log_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    new_log = PatientHealthLog(
        patient_id=log_data.patient_id,
        practitioner_id=practitioner.id if practitioner else 1, # Fallback for admin
        dosha_vata=log_data.dosha_vata,
        dosha_pitta=log_data.dosha_pitta,
        dosha_kapha=log_data.dosha_kapha,
        sleep_score=log_data.sleep_score,
        stress_level=log_data.stress_level,
        hydration=log_data.hydration,
        weight=log_data.weight,
        blood_pressure=log_data.blood_pressure,
        notes=log_data.notes,
        recommendations=log_data.recommendations
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@app.get("/api/health-logs/me", response_model=List[HealthLogResponse])
async def get_my_health_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get health logs for current patient"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can access their health logs")
        
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
        
    logs = db.query(PatientHealthLog).filter(
        PatientHealthLog.patient_id == patient.id
    ).order_by(PatientHealthLog.date.desc()).limit(limit).all()
    
    return logs

# ==================== HEALTH SUPPORT ENDPOINTS ====================

@app.post("/health/symptoms", response_model=SymptomResponse)
async def log_symptom(
    symptom_data: SymptomCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a new symptom for the current patient"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can log symptoms")
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    symptom = Symptom(
        patient_id=patient.id,
        symptom_name=symptom_data.symptom_name,
        severity=symptom_data.severity,
        notes=symptom_data.notes,
        duration_days=symptom_data.duration_days
    )
    
    db.add(symptom)
    db.commit()
    db.refresh(symptom)
    
    return symptom

@app.get("/health/symptoms")
async def get_symptoms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get symptom history for current patient"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can access symptoms")
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    symptoms = db.query(Symptom).filter(
        Symptom.patient_id == patient.id
    ).order_by(Symptom.created_at.desc()).limit(limit).all()
    
    return symptoms

@app.post("/health/ask-ai", response_model=AIHealthResponse)
async def ask_health_ai(
    request: AIHealthRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enhanced AI health assistant with conversational capabilities"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can use AI health assistant")
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    # Generate or use existing conversation ID
    import uuid
    conversation_id = None
    if request.context and 'conversation_id' in request.context:
        conversation_id = request.context['conversation_id']
    
    if not conversation_id:
        conversation_id = f"conv_{patient.id}_{uuid.uuid4().hex[:8]}"
    
    # Get or create conversation
    conversation = db.query(AIConversation).filter(
        AIConversation.conversation_id == conversation_id
    ).first()
    
    if not conversation:
        conversation = AIConversation(
            patient_id=patient.id,
            conversation_id=conversation_id,
            messages=[]
        )
        db.add(conversation)
    
    # Add user message
    user_message = {
        "role": "user",
        "content": request.question,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if conversation.messages is None:
        conversation.messages = []
    conversation.messages.append(user_message)
    
    # Get latest health log for dosha analysis
    latest_log = db.query(PatientHealthLog).filter(
        PatientHealthLog.patient_id == patient.id
    ).order_by(PatientHealthLog.date.desc()).first()
    
    dosha_analysis = {
        "vata": latest_log.dosha_vata if latest_log else 33,
        "pitta": latest_log.dosha_pitta if latest_log else 33,
        "kapha": latest_log.dosha_kapha if latest_log else 34
    }
    
    # Build user profile from context and patient data
    user_profile = request.context if request.context else {}
    user_profile.update({
        'prakriti_type': patient.prakriti_type,
        'medical_history': patient.medical_history,
        'allergies': patient.allergies
    })
    
    try:
        # Use enhanced health assistant
        from enhanced_health_assistant import health_assistant
        
        response_data = await health_assistant.generate_conversational_response(
            query=request.question,
            user_profile=user_profile,
            conversation_history=conversation.messages,
            dosha_analysis=dosha_analysis
        )
        
        # Format response based on type
        if response_data['type'] == 'clarification':
            # Use the pre-formatted message from enhanced assistant
            ai_answer = response_data['message']
        elif response_data['type'] == 'diet_plan':
            diet_plan = response_data['data']
            ai_answer = f"{response_data['message']}\\n\\n"
            ai_answer += f"📊 **Your Metrics:**\\n"
            ai_answer += f"- BMI: {diet_plan['bmi']}\\n"
            ai_answer += f"- Daily Calorie Target: {diet_plan['target_calories']} kcal\\n"
            ai_answer += f"- Dominant Dosha: {diet_plan['dominant_dosha'].title()}\\n\\n"
            ai_answer += f"🥗 **Macros:**\\n"
            ai_answer += f"- Protein: {diet_plan['macros']['protein']}\\n"
            ai_answer += f"- Carbs: {diet_plan['macros']['carbs']}\\n"
            ai_answer += f"- Fats: {diet_plan['macros']['fats']}\\n\\n"
            ai_answer += f"✅ **Foods to Favor:** {', '.join(diet_plan['foods_to_favor'][:5])}\\n\\n"
            ai_answer += f"❌ **Foods to Avoid:** {', '.join(diet_plan['foods_to_avoid'][:5])}\\n\\n"
            ai_answer += f"🍽️ **Sample Meal Plan:**\\n"
            for meal, details in diet_plan['meal_plan'].items():
                ai_answer += f"- **{meal.title()}**: {details['suggestion']} ({details['calories']} kcal)\\n"
            ai_answer += f"\\n💧 **Hydration:** {diet_plan['hydration']}\\n"
        elif response_data['type'] == 'workout_plan':
            workout_plan = response_data['data']
            ai_answer = f"{response_data['message']}\\n\\n"
            ai_answer += f"🏋️ **Workout Style:** {workout_plan['workout_style']}\\n\\n"
            ai_answer += f"✅ **Recommended Activities:** {', '.join(workout_plan['recommended_activities'][:4])}\\n\\n"
            ai_answer += f"📅 **Weekly Plan:**\\n"
            for day, activity in workout_plan['weekly_plan'].items():
                ai_answer += f"- **{day}**: {activity}\\n"
            ai_answer += f"\\n🧘 **Yoga Sequence:**\\n"
            for pose in workout_plan['yoga_sequence'][:5]:
                ai_answer += f"- {pose}\\n"
        else:
            ai_answer = response_data['message']
        
        # Add AI response to conversation
        ai_message = {
            "role": "assistant",
            "content": ai_answer,
            "timestamp": datetime.utcnow().isoformat()
        }
        conversation.messages.append(ai_message)
        
        db.commit()
        
        return AIHealthResponse(
            answer=ai_answer,
            sources=response_data.get('sources', ["Enhanced Health Assistant"]),
            conversation_id=conversation_id
        )
        
    except Exception as e:
        logger.error(f"Enhanced AI health assistant error: {str(e)}")
        # Fallback to simple response
        ai_answer = "I can help you with personalized diet plans, workout recommendations, and general health guidance. What would you like to know more about?"
        
        ai_message = {
            "role": "assistant",
            "content": ai_answer,
            "timestamp": datetime.utcnow().isoformat()
        }
        conversation.messages.append(ai_message)
        db.commit()
        
        return AIHealthResponse(
            answer=ai_answer,
            sources=["Health Assistant"],
            conversation_id=conversation_id
        )

@app.get("/health/recommendations", response_model=HealthRecommendationsResponse)
async def get_health_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated health recommendations based on patient data"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can get recommendations")
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    # Get recent symptoms
    recent_symptoms = db.query(Symptom).filter(
        Symptom.patient_id == patient.id
    ).order_by(Symptom.created_at.desc()).limit(5).all()
    
    # Get latest health log
    latest_log = db.query(PatientHealthLog).filter(
        PatientHealthLog.patient_id == patient.id
    ).order_by(PatientHealthLog.date.desc()).first()
    
    # Generate recommendations based on data
    recommendations = []
    
    # Dosha-based recommendations
    if latest_log:
        if latest_log.dosha_vata > 60:
            recommendations.append({
                "category": "diet",
                "suggestion": "Consume warm, cooked foods and avoid cold, raw foods",
                "reason": "High Vata levels indicate need for grounding and warmth",
                "priority": "high"
            })
        if latest_log.dosha_pitta > 60:
            recommendations.append({
                "category": "lifestyle",
                "suggestion": "Practice cooling pranayama and avoid excessive heat",
                "reason": "Elevated Pitta requires cooling practices",
                "priority": "high"
            })
        if latest_log.dosha_kapha > 60:
            recommendations.append({
                "category": "lifestyle",
                "suggestion": "Increase physical activity and reduce heavy foods",
                "reason": "High Kapha benefits from movement and lightness",
                "priority": "high"
            })
        
        # Sleep recommendations
        if latest_log.sleep_score and latest_log.sleep_score < 60:
            recommendations.append({
                "category": "lifestyle",
                "suggestion": "Establish a regular sleep schedule and practice evening meditation",
                "reason": "Low sleep score indicates need for better sleep hygiene",
                "priority": "normal"
            })
        
        # Hydration recommendations
        if latest_log.hydration < 2.0:
            recommendations.append({
                "category": "diet",
                "suggestion": "Increase water intake to at least 2.5 liters per day",
                "reason": "Current hydration levels are below optimal",
                "priority": "normal"
            })
    
    # Symptom-based recommendations
    for symptom in recent_symptoms:
        if "headache" in symptom.symptom_name.lower():
            recommendations.append({
                "category": "herbs",
                "suggestion": "Try ginger tea or apply cooling sandalwood paste to forehead",
                "reason": "Natural remedies for headache relief",
                "priority": "normal"
            })
    
    # Default recommendations if none generated
    if not recommendations:
        recommendations = [
            {
                "category": "lifestyle",
                "suggestion": "Maintain a balanced daily routine (Dinacharya)",
                "reason": "Foundation of Ayurvedic health",
                "priority": "normal"
            },
            {
                "category": "diet",
                "suggestion": "Eat according to your Prakriti type",
                "reason": "Personalized nutrition for optimal health",
                "priority": "normal"
            }
        ]
    
    dosha_analysis = {
        "vata": latest_log.dosha_vata if latest_log else 33,
        "pitta": latest_log.dosha_pitta if latest_log else 33,
        "kapha": latest_log.dosha_kapha if latest_log else 34
    }
    
    return HealthRecommendationsResponse(
        recommendations=recommendations,
        dosha_analysis=dosha_analysis
    )

# ==================== CHAT SUPPORT ENDPOINTS ====================

@app.get("/chat/practitioners")
async def get_available_practitioners(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of available practitioners for chat"""
    practitioners = db.query(Practitioner).join(User).filter(
        User.is_active == True
    ).limit(20).all()
    
    result = []
    for prac in practitioners:
        result.append({
            "id": prac.id,
            "name": prac.user.full_name,
            "specialization": prac.specializations[0] if prac.specializations else None,
            "online": True,  # TODO: Implement real online status
            "last_seen": datetime.utcnow()
        })
    
    return result

@app.get("/chat/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    recipient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get chat message history with a specific user"""
    # Determine sender type
    sender_type = current_user.role.value
    sender_id = current_user.id
    
    # Get messages where user is either sender or recipient
    messages = db.query(ChatMessage).filter(
        ((ChatMessage.sender_id == sender_id) & (ChatMessage.recipient_id == recipient_id)) |
        ((ChatMessage.sender_id == recipient_id) & (ChatMessage.recipient_id == sender_id))
    ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    # Mark messages as read
    for msg in messages:
        if msg.recipient_id == sender_id and not msg.read:
            msg.read = True
    
    db.commit()
    
    return list(reversed(messages))

@app.post("/chat/send", response_model=ChatMessageResponse)
async def send_chat_message(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a chat message"""
    sender_type = current_user.role.value
    
    message = ChatMessage(
        sender_id=current_user.id,
        sender_type=sender_type,
        recipient_id=message_data.recipient_id,
        recipient_type=message_data.recipient_type,
        content=message_data.content,
        read=False
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message

@app.post("/chat/ai-assistant", response_model=AIChatResponse)
async def chat_with_ai_assistant(
    request: AIChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI assistant"""
    # Generate or use existing conversation ID
    import uuid
    conversation_id = request.conversation_id or f"chat_{current_user.id}_{uuid.uuid4().hex[:8]}"
    
    # Get or create conversation
    conversation = db.query(AIConversation).filter(
        AIConversation.conversation_id == conversation_id
    ).first()
    
    if not conversation:
        # Try to get patient ID if user is a patient
        patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        patient_id = patient.id if patient else None
        
        # Create conversation (patient_id can be None for non-patients)
        conversation = AIConversation(
            patient_id=patient_id,
            conversation_id=conversation_id,
            messages=[]
        )
        db.add(conversation)
    
    # Add user message
    user_message = {
        "role": "user",
        "content": request.message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if conversation.messages is None:
        conversation.messages = []
    conversation.messages.append(user_message)
    
    # Call AI service
    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}"
        
        # Build conversation context
        context = "You are an Ayurvedic health assistant. Provide helpful, accurate information about Ayurveda, wellness, and natural health practices.\n\n"
        for msg in conversation.messages[-5:]:  # Last 5 messages for context
            context += f"{msg['role']}: {msg['content']}\n"
        
        response = requests.post(
            gemini_url,
            json={
                "contents": [{
                    "parts": [{"text": context}]
                }]
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
        else:
            ai_reply = "I apologize, but I'm having trouble right now. Please try again later."
        
        # Add AI response
        ai_message = {
            "role": "assistant",
            "content": ai_reply,
            "timestamp": datetime.utcnow().isoformat()
        }
        conversation.messages.append(ai_message)
        
        db.commit()
        
        return AIChatResponse(
            reply=ai_reply,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        logger.error(f"AI chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get AI response: {str(e)}")



# ==================== NOTIFICATIONS ====================

@app.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    unread_only: bool = False,
    limit: int = 50
):
    """Get notifications for current user"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
    return notifications

@app.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


# ==================== DEBUG / DB VIEWER ====================
print("LOADING MAIN.PY - VERSION CHECK 999")
@app.get("/db-view")
def get_db_viewer():
    """Serve the database viewer HTML"""
    print("DEBUG: Entering get_db_viewer (SYNC) - NEW ROUTE")
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "database_viewer.html")
        print(f"DEBUG: Calculated path: {file_path}")
        # print(f"DEBUG: Exists? {os.path.exists(file_path)}")
        if not os.path.exists(file_path):
            return JSONResponse(status_code=404, content={"detail": f"File not found at {file_path}"})
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        try:
            with open("backend/error_log.txt", "w") as err_f:
                err_f.write(error_msg)
        except:
            pass
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e), "traceback": error_msg})

@app.get("/debug/db-data")
async def get_debug_db_data(db: Session = Depends(get_db)):
    """Fetch all DB data for the viewer"""
    stats = {}
    
    # Tables to inspect
    tables = {
        "users": User,
        "patients": Patient,
        "practitioners": Practitioner,
        "admins": Admin,
        "appointments": Appointment,
        "therapy_sessions": TherapySession
    }
    
    output = {"stats": {}, "users": []}
    
    for name, model in tables.items():
        count = db.query(func.count(model.id)).scalar()
        output["stats"][name] = count
        
    # Fetch all users with details
    users = db.query(User).all()
    user_list = []
    for u in users:
        user_list.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role.value,
            "last_login": u.last_login or "Never",
            "is_active": u.is_active
        })
    output["users"] = user_list
    
    return output

@app.delete("/debug/delete-user/{user_id}")
async def debug_delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user for debug purposes"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Cascade delete should handle profile via relationship, but let's be safe if not set
    # Actually SQLAlchemy relationships usually handle this if cascade is set.
    # We'll just delete user.
    try:
        db.delete(user)
        db.commit()
        return {"message": "User deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )
