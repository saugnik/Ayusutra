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
    created_at: string;
}

// ==================== AVAILABILITY TYPES ====================
export interface AvailabilitySlot {
    start_time: string;
    end_time: string;
    location?: string;
}

export interface AvailabilitySchedule {
    monday: AvailabilitySlot[];
    tuesday: AvailabilitySlot[];
    wednesday: AvailabilitySlot[];
    thursday: AvailabilitySlot[];
    friday: AvailabilitySlot[];
    saturday: AvailabilitySlot[];
    sunday: AvailabilitySlot[];
}

// ==================== PRACTITIONER TYPES ====================
export interface PractitionerUser {
    full_name: string;
    email: string;
    phone?: string;
    profile_picture?: string;
}

export interface Practitioner {
    id: number;
    user_id: number;
    license_number?: string;
    specializations: string[];
    experience_years: number;
    qualification?: string;
    clinic_name?: string;
    clinic_address?: string;
    latitude?: number;
    longitude?: number;
    consultation_fee: number;
    availability_schedule?: AvailabilitySchedule;
    bio?: string;
    rating: number;
    total_reviews: number;
    is_verified: boolean;
    created_at: string;
    user?: PractitionerUser;
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
    action_url?: string;
    created_at: string;
}

// ==================== HEALTH LOG TYPES ====================
export interface HealthLog {
    id: number;
    patient_id: number;
    practitioner_id: number;
    date: string;
    dosha_vata: number;
    dosha_pitta: number;
    dosha_kapha: number;
    sleep_score?: number;
    stress_level?: string;
    hydration?: number;
    weight?: number;
    blood_pressure?: string;
    notes?: string;
    recommendations?: string;
    created_at: string;
}

export interface HealthLogCreate {
    patient_id: number;
    dosha_vata: number;
    dosha_pitta: number;
    dosha_kapha: number;
    sleep_score?: number;
    stress_level?: string;
    hydration?: number;
    weight?: number;
    blood_pressure?: string;
    notes?: string;
    recommendations?: string;
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

export interface PatientListItem {
    id: number;
    name: string;
    age?: number;
    gender?: string;
    phone?: string;
    email: string;
    current_therapy?: string;
    stage?: string;
    next_appointment?: string;
    status: string;
    prakriti?: string;
}

// ==================== NOTIFICATION TYPES ====================
export interface Notification {
    id: number | string;
    user_id?: number;
    title: string;
    message: string;
    type: 'reminder' | 'alert' | 'info' | 'appointment' | 'system';
    priority?: 'low' | 'normal' | 'high' | 'urgent';
    is_read?: boolean;
    read?: boolean; // For compatibility with local component state
    action_url?: string;
    expires_at?: string;
    created_at?: string;
    time?: string; // For compatibility with local component state
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

// ==================== REPORT TYPES ====================
export interface ReportHealthStats {
    average_sleep?: number;
    average_hydration?: number;
    stress_trend?: string;
    dominant_dosha?: string;
}

export interface PatientReportResponse {
    generated_at: string;
    patient_name: string;
    patient_age?: number;
    patient_gender?: string;
    prakriti_type?: string;
    health_stats: ReportHealthStats;
    recent_appointments: AppointmentResponse[];
    recent_health_logs: HealthLog[];
    doctor_notes?: string;
}

export interface TreatmentTypeStat {
    type: string;
    count: number;
    success_rate: number;
}

export interface TreatmentAnalyticsResponse {
    total_treatments: number;
    success_rate_overall: number;
    type_distribution: TreatmentTypeStat[];
    monthly_trends: Array<{ month: string; count: number }>;
}

export interface MonthlySummaryResponse {
    month: string;
    total_revenue: number;
    total_appointments: number;
    new_patients: number;
    popular_therapies: string[];
    appointment_status_counts: Record<string, number>;
}

export interface FeedbackSummary {
    average_rating: number;
    total_reviews: number;
    rating_distribution: Record<number, number>;
    recent_feedback: Feedback[];
}

export interface FeedbackReportResponse {
    summary: FeedbackSummary;
    improvement_areas: string[];
}

// ==================== API ERROR TYPES ====================
export interface APIError {
    detail: string;
    status?: number;
}
