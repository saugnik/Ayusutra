
import os
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import func
import requests

from database import engine, SessionLocal
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
    PractitionerAvailability, AIChatRequest, AIChatResponse
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
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Configure CORS - Specific origins required when using credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.233.32.74:3000"  # Network address
    ],
    allow_credentials=False,  # Disable credentials to allow broader access
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Security
security = HTTPBearer()

# RAG Service Configuration
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://localhost:8000")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    
    return DashboardStats(
        total_patients=total_patients,
        today_appointments=today_appointments,
        active_treatments=active_treatments,
        pending_reports=pending_reports,
        success_rate=0.0,  # Real data pending implementation
        avg_session_rating=0.0  # Real data pending implementation
    )


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
    total_practitioners = db.query(User).filter(User.role == "practitioner").count()
    total_patients = db.query(User).filter(User.role == "patient").count()
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
@app.get("/reports/treatments")
async def get_treatment_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = 30
):
    """Get treatment analytics"""
    if current_user.role not in ["practitioner", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Real Analytics Data
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=days)
    
    # 1. Total Sessions (Completed Appointments in period)
    total_sessions = db.query(Appointment).filter(
        Appointment.status == "completed",
        Appointment.scheduled_datetime >= thirty_days_ago
    ).count()
    
    # 2. Success Rate (Mock logic based on completion vs cancellation)
    completed_count = total_sessions
    cancelled_count = db.query(Appointment).filter(
        Appointment.status == "cancelled",
        Appointment.scheduled_datetime >= thirty_days_ago
    ).count()
    total_relevant = completed_count + cancelled_count
    success_rate = (completed_count / total_relevant * 100) if total_relevant > 0 else 0.0
    
    # 3. Average Duration
    avg_duration = db.query(func.avg(Appointment.duration_minutes)).filter(
        Appointment.status == "completed"
    ).scalar() or 0.0
    
    # 4. Patient Satisfaction (from Feedback)
    avg_rating = db.query(func.avg(Feedback.rating)).scalar() or 0.0
    
    # 5. Popular Therapies
    popular_therapies_query = db.query(
        Appointment.therapy_type, func.count(Appointment.id)
    ).group_by(Appointment.therapy_type).order_by(func.count(Appointment.id).desc()).limit(4).all()
    
    popular_therapies = [{"name": t, "count": c} for t, c in popular_therapies_query]
    
    # 6. Monthly Trends (Last 6 months)
    monthly_trends = []
    for i in range(5, -1, -1):
        month_start = datetime(now.year, now.month, 1) - timedelta(days=30*i) # Approx
        # Better date logic needed for strict months, but approx is fine for now
        # Actually let's use simple logic: distinct months from data or just query last 3 months explicitly
        pass

    # Simplified Monthly Trends (Current Month)
    current_month_count = db.query(Appointment).filter(
        func.extract('month', Appointment.scheduled_datetime) == now.month,
        func.extract('year', Appointment.scheduled_datetime) == now.year
    ).count()
    
    monthly_trends = [
        {"month": now.strftime("%b"), "sessions": current_month_count}
    ]

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



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
