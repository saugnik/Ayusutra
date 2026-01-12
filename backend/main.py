

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
from models import User, Patient, Practitioner, Admin, Appointment, TherapySession, Feedback, UserRole, Base, Notification, SystemSettings, AuditLog
from schemas import (
    UserCreate, UserResponse, UserLogin, TokenResponse,
    PatientCreate, PatientResponse, PatientUpdate,
    PractitionerCreate, PractitionerResponse, PractitionerUpdate,
    AdminCreate, AdminResponse,
    AppointmentCreate, AppointmentResponse, AppointmentUpdate,
    TherapySessionCreate, TherapySessionResponse,
    FeedbackCreate, FeedbackResponse,
    AIAssistantRequest, AIAssistantResponse,
    DashboardStats
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


@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)


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
        success_rate=94.5,  # Mock data
        avg_session_rating=4.8  # Mock data
    )


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
    
    # Mock analytics data
    return {
        "total_sessions": 156,
        "success_rate": 94.5,
        "average_duration": 75.5,
        "patient_satisfaction": 4.8,
        "popular_therapies": [
            {"name": "Abhyanga", "count": 45},
            {"name": "Shirodhara", "count": 32},
            {"name": "Nasya", "count": 28},
            {"name": "Virechana", "count": 25}
        ],
        "monthly_trends": [
            {"month": "Jan", "sessions": 120},
            {"month": "Feb", "sessions": 135},
            {"month": "Mar", "sessions": 156}
        ]
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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
