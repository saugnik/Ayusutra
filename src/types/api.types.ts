/**
 * TypeScript Interfaces for API Responses
 * Matches backend Pydantic schemas
 */

// ==================== USER TYPES ====================
export interface User {
    id: number;
    email: string;
    full_name: string;
    role: 'patient' | 'practitioner' | 'admin';
    phone?: string;
    profile_picture?: string;
    is_active: boolean;
    is_verified: boolean;
    created_at: string;
    last_login?: string;
}

export interface UserCreate {
    email: string;
    full_name: string;
    password: string;
    role: 'patient' | 'practitioner' | 'admin';
    phone?: string;
    // Patient fields
    date_of_birth?: string;
    gender?: string;
    address?: string;
    emergency_contact?: string;
    // Practitioner fields
    license_number?: string;
    specializations?: string[];
    experience_years?: number;
    clinic_name?: string;
    clinic_address?: string;
    consultation_fee?: number;
}

export interface UserLogin {
    email: string;
    password: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
    user_id: number;
    role: string;
    full_name: string;
}

// ==================== PATIENT TYPES ====================
export interface Patient {
    id: number;
    user_id: number;
    date_of_birth?: string;
    gender?: string;
    address?: string;
    emergency_contact?: string;
    medical_history: string[];
    current_medications: string[];
    allergies: string[];
    prakriti_type?: string;
    lifestyle_preferences: Record<string, any>;
    created_at: string;
}

// ==================== PRACTITIONER TYPES ====================
export interface Practitioner {
    id: number;
    user_id: number;
    license_number?: string;
    specializations: string[];
    experience_years: number;
    qualification?: string;
    clinic_name?: string;
    clinic_address?: string;
    consultation_fee: number;
    bio?: string;
    rating: number;
    total_reviews: number;
    is_verified: boolean;
    created_at: string;
    user?: {
        full_name: string;
        email: string;
        profile_picture?: string;
    };
}

// ==================== APPOINTMENT TYPES ====================
export interface AppointmentResponse {
    id: number;
    patient_id: number;
    practitioner_id: number;
    therapy_type: string;
    scheduled_datetime: string;
    duration_minutes: number;
    status: 'scheduled' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled' | 'no_show';
    notes?: string;
    patient_notes?: string;
    practitioner_notes?: string;
    fee?: number;
    payment_status: string;
    created_at: string;
    updated_at?: string;
}

export type Appointment = AppointmentResponse;

export interface AppointmentCreate {
    patient_id: number;
    practitioner_id: number;
    therapy_type: string;
    scheduled_datetime: string;
    duration_minutes?: number;
    notes?: string;
}

// ==================== FEEDBACK TYPES ====================
export interface Feedback {
    id: number;
    patient_id: number;
    practitioner_id: number;
    appointment_id?: number;
    rating: number;
    satisfaction_level?: string;
    comments?: string;
    therapy_effectiveness?: number;
    practitioner_professionalism?: number;
    facility_cleanliness?: number;
    would_recommend?: boolean;
    suggestions?: string;
    created_at: string;
}

export interface FeedbackCreate {
    patient_id: number;
    practitioner_id: number;
    appointment_id?: number;
    rating: number;
    satisfaction_level?: string;
    comments?: string;
}

// ==================== DASHBOARD TYPES ====================
export interface DashboardStats {
    // Patient dashboard
    total_appointments?: number;
    upcoming_appointments?: number;
    completed_sessions?: number;
    active_treatments?: number;
    patient_satisfaction?: number;
    avg_session_duration?: number;

    // Practitioner dashboard
    total_patients?: number;
    today_appointments?: number;
    pending_reports?: number;
    success_rate?: number;
    avg_session_rating?: number;

    // Admin dashboard
    total_users?: number;
    total_practitioners?: number;
    recent_registrations?: number;
    system_health?: number;
}

// ==================== AI ASSISTANT TYPES ====================
export interface AIAssistantRequest {
    query: string;
    top_k?: number;
}

export interface AIAssistantResponse {
    query: string;
    answer: Record<string, any>;
    context: Array<Record<string, any>>;
    confidence: string;
    sources: Array<Record<string, any>>;
}

// ==================== API ERROR TYPES ====================
export interface APIError {
    detail: string;
    status?: number;
}
