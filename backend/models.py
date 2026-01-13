"""
Database Models for AyurSutra Backend
SQLAlchemy models for all entities in the system.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    PATIENT = "patient"
    PRACTITIONER = "practitioner"
    ADMIN = "admin"

class AppointmentStatus(enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    phone = Column(String(20), nullable=True)
    profile_picture = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    patient_profile = relationship("Patient", back_populates="user", uselist=False, cascade="all, delete-orphan")
    practitioner_profile = relationship("Practitioner", back_populates="user", uselist=False, cascade="all, delete-orphan")
    admin_profile = relationship("Admin", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact = Column(String(255), nullable=True)
    medical_history = Column(JSON, default=list)  # List of medical conditions
    current_medications = Column(JSON, default=list)  # List of current medications
    allergies = Column(JSON, default=list)  # List of allergies
    prakriti_type = Column(String(50), nullable=True)  # Vata, Pitta, Kapha, Mixed
    lifestyle_preferences = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")
    therapy_sessions = relationship("TherapySession", back_populates="patient")
    feedback = relationship("Feedback", back_populates="patient")

class Practitioner(Base):
    __tablename__ = "practitioners"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    license_number = Column(String(100), unique=True, nullable=True)
    specializations = Column(JSON, default=list)  # List of specializations
    experience_years = Column(Integer, default=0)
    qualification = Column(String(255), nullable=True)
    clinic_name = Column(String(255), nullable=True)
    clinic_address = Column(Text, nullable=True)
    consultation_fee = Column(Float, default=0.0)
    availability_schedule = Column(JSON, default=dict)  # Weekly schedule
    bio = Column(Text, nullable=True)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="practitioner_profile")
    appointments = relationship("Appointment", back_populates="practitioner")
    therapy_sessions = relationship("TherapySession", back_populates="practitioner")
    feedback = relationship("Feedback", back_populates="practitioner")

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    admin_level = Column(String(20), default="standard")  # standard, senior, super
    permissions = Column(JSON, default=list)  # List of permissions
    department = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="admin_profile")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    practitioner_id = Column(Integer, ForeignKey("practitioners.id"), nullable=False)
    therapy_type = Column(String(100), nullable=False)
    scheduled_datetime = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    notes = Column(Text, nullable=True)
    patient_notes = Column(Text, nullable=True)
    practitioner_notes = Column(Text, nullable=True)
    fee = Column(Float, nullable=True)
    payment_status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    practitioner = relationship("Practitioner", back_populates="appointments")
    therapy_session = relationship("TherapySession", back_populates="appointment", uselist=False)
    feedback = relationship("Feedback", back_populates="appointment", uselist=False)

class TherapySession(Base):
    __tablename__ = "therapy_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    practitioner_id = Column(Integer, ForeignKey("practitioners.id"), nullable=False)
    therapy_type = Column(String(100), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="scheduled")  # scheduled, in_progress, completed, cancelled
    pre_session_notes = Column(Text, nullable=True)
    session_notes = Column(Text, nullable=True)
    post_session_notes = Column(Text, nullable=True)
    vitals_before = Column(JSON, default=dict)  # Blood pressure, pulse, etc.
    vitals_after = Column(JSON, default=dict)
    therapy_parameters = Column(JSON, default=dict)  # Temperature, duration, oils used, etc.
    patient_feedback_during = Column(Text, nullable=True)
    complications = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    next_session_recommendations = Column(Text, nullable=True)
    report = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    appointment = relationship("Appointment", back_populates="therapy_session")
    patient = relationship("Patient", back_populates="therapy_sessions")
    practitioner = relationship("Practitioner", back_populates="therapy_sessions")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    practitioner_id = Column(Integer, ForeignKey("practitioners.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5 rating
    satisfaction_level = Column(String(20), nullable=True)  # very_satisfied, satisfied, neutral, dissatisfied, very_dissatisfied
    comments = Column(Text, nullable=True)
    therapy_effectiveness = Column(Integer, nullable=True)  # 1-5 rating
    practitioner_professionalism = Column(Integer, nullable=True)  # 1-5 rating
    facility_cleanliness = Column(Integer, nullable=True)  # 1-5 rating
    would_recommend = Column(Boolean, nullable=True)
    suggestions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="feedback")
    practitioner = relationship("Practitioner", back_populates="feedback")
    appointment = relationship("Appointment", back_populates="feedback")

class TherapyTemplate(Base):
    __tablename__ = "therapy_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # Panchakarma, Massage, etc.
    duration_minutes = Column(Integer, default=60)
    preparation_steps = Column(JSON, default=list)
    procedure_steps = Column(JSON, default=list)
    post_care_instructions = Column(JSON, default=list)
    contraindications = Column(JSON, default=list)
    required_materials = Column(JSON, default=list)
    benefits = Column(JSON, default=list)
    suitable_conditions = Column(JSON, default=list)
    cost_range = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("practitioners.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # appointment, reminder, system, alert
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    is_read = Column(Boolean, default=False)
    action_url = Column(String(500), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)
    is_public = Column(Boolean, default=False)  # Can be accessed by frontend
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PatientHealthLog(Base):
    __tablename__ = "patient_health_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    practitioner_id = Column(Integer, ForeignKey("practitioners.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ayurvedic Metrics
    dosha_vata = Column(Integer, default=50) # 0-100
    dosha_pitta = Column(Integer, default=50)
    dosha_kapha = Column(Integer, default=50)
    
    # General Metrics
    sleep_score = Column(Integer, nullable=True) # 0-100
    stress_level = Column(String(50), default="Medium") # Low, Medium, High
    hydration = Column(Float, default=0.0) # Liters
    weight = Column(Float, nullable=True)
    blood_pressure = Column(String(20), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient")
    practitioner = relationship("Practitioner")

class Symptom(Base):
    """Patient symptom logs for health tracking"""
    __tablename__ = "symptoms"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    symptom_name = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False)  # low, moderate, high, severe
    notes = Column(Text, nullable=True)
    duration_days = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    patient = relationship("Patient", backref="symptoms")

class AIConversation(Base):
    """Store AI health assistant conversations"""
    __tablename__ = "ai_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    conversation_id = Column(String(255), unique=True, nullable=False, index=True)
    messages = Column(JSON, nullable=False, default=list)  # Array of {role, content, timestamp}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    patient = relationship("Patient", backref="ai_conversations")

class ChatMessage(Base):
    """Messages between patients and practitioners"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    sender_type = Column(String(50), nullable=False)  # 'patient' or 'practitioner'
    recipient_id = Column(Integer, nullable=False)
    recipient_type = Column(String(50), nullable=False)  # 'patient' or 'practitioner'
    content = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
