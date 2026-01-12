# AyurSutra Database Structure

## Database Overview

- **Database File**: `ayursutra.db`
- **Type**: SQLite
- **Size**: 128 KB
- **Total Tables**: 11
- **Current Status**: Empty (ready for data)

---

## Table Summary

| Table Name | Columns | Rows | Status |
|------------|---------|------|--------|
| admins | 7 | 0 | EMPTY |
| appointments | 16 | 0 | EMPTY |
| audit_logs | 8 | 0 | EMPTY |
| feedback | 13 | 0 | EMPTY |
| notifications | 9 | 0 | EMPTY |
| patients | 12 | 0 | EMPTY |
| practitioners | 14 | 0 | EMPTY |
| system_settings | 7 | 0 | EMPTY |
| therapy_sessions | 17 | 0 | EMPTY |
| therapy_templates | 14 | 0 | EMPTY |
| users | 11 | 0 | EMPTY |

---

## Detailed Table Schemas

### 1. USERS Table
**Purpose**: Main user accounts for all roles

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| full_name | VARCHAR(255) | NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL |
| role | VARCHAR(15) | NOT NULL (patient/practitioner/admin) |
| phone | VARCHAR(20) | |
| profile_picture | VARCHAR(500) | |
| is_active | BOOLEAN | DEFAULT TRUE |
| is_verified | BOOLEAN | DEFAULT FALSE |
| created_at | DATETIME | |
| last_login | DATETIME | |

**Relationships**:
- One-to-one with patients, practitioners, or admins

---

### 2. PATIENTS Table
**Purpose**: Patient-specific profile information

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users.id, UNIQUE |
| date_of_birth | DATETIME | |
| gender | VARCHAR(10) | |
| address | TEXT | |
| emergency_contact | VARCHAR(255) | |
| medical_history | JSON | List of conditions |
| current_medications | JSON | List of medications |
| allergies | JSON | List of allergies |
| prakriti_type | VARCHAR(50) | Vata/Pitta/Kapha |
| lifestyle_preferences | JSON | |
| created_at | DATETIME | |

**Relationships**:
- Belongs to one user
- Has many appointments
- Has many therapy sessions
- Has many feedback entries

---

### 3. PRACTITIONERS Table
**Purpose**: Practitioner/doctor profile information

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users.id, UNIQUE |
| license_number | VARCHAR(100) | UNIQUE |
| specializations | JSON | List of specializations |
| experience_years | INTEGER | |
| qualification | VARCHAR(255) | |
| clinic_name | VARCHAR(255) | |
| clinic_address | TEXT | |
| consultation_fee | FLOAT | |
| availability_schedule | JSON | Weekly schedule |
| bio | TEXT | |
| rating | FLOAT | Average rating |
| total_reviews | INTEGER | |
| is_verified | BOOLEAN | |

**Relationships**:
- Belongs to one user
- Has many appointments
- Has many therapy sessions
- Has many feedback entries

---

### 4. ADMINS Table
**Purpose**: Administrator accounts

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users.id, UNIQUE |
| admin_level | VARCHAR(20) | standard/senior/super |
| permissions | JSON | List of permissions |
| department | VARCHAR(100) | |
| created_at | DATETIME | |

---

### 5. APPOINTMENTS Table
**Purpose**: Appointment bookings between patients and practitioners

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| patient_id | INTEGER | FOREIGN KEY → patients.id |
| practitioner_id | INTEGER | FOREIGN KEY → practitioners.id |
| therapy_type | VARCHAR(100) | NOT NULL |
| scheduled_datetime | DATETIME | NOT NULL |
| duration_minutes | INTEGER | DEFAULT 60 |
| status | VARCHAR(20) | scheduled/confirmed/in_progress/completed/cancelled |
| notes | TEXT | |
| patient_notes | TEXT | |
| practitioner_notes | TEXT | |
| fee | FLOAT | |
| payment_status | VARCHAR(20) | DEFAULT pending |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| created_by | INTEGER | FOREIGN KEY → users.id |

**Relationships**:
- Belongs to one patient
- Belongs to one practitioner
- Has one therapy session
- Has one feedback entry

---

### 6. THERAPY_SESSIONS Table
**Purpose**: Detailed therapy session records

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| appointment_id | INTEGER | FOREIGN KEY → appointments.id, UNIQUE |
| patient_id | INTEGER | FOREIGN KEY → patients.id |
| practitioner_id | INTEGER | FOREIGN KEY → practitioners.id |
| therapy_type | VARCHAR(100) | |
| start_time | DATETIME | |
| end_time | DATETIME | |
| status | VARCHAR(20) | |
| pre_session_notes | TEXT | |
| session_notes | TEXT | |
| post_session_notes | TEXT | |
| vitals_before | JSON | BP, pulse, etc. |
| vitals_after | JSON | |
| therapy_parameters | JSON | Temperature, oils, etc. |
| patient_feedback_during | TEXT | |
| complications | TEXT | |
| recommendations | TEXT | |
| report | TEXT | |

---

### 7. FEEDBACK Table
**Purpose**: Patient feedback and ratings

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| patient_id | INTEGER | FOREIGN KEY → patients.id |
| practitioner_id | INTEGER | FOREIGN KEY → practitioners.id |
| appointment_id | INTEGER | FOREIGN KEY → appointments.id |
| rating | INTEGER | 1-5 stars |
| satisfaction_level | VARCHAR(20) | |
| comments | TEXT | |
| therapy_effectiveness | INTEGER | 1-5 |
| practitioner_professionalism | INTEGER | 1-5 |
| facility_cleanliness | INTEGER | 1-5 |
| would_recommend | BOOLEAN | |
| suggestions | TEXT | |
| created_at | DATETIME | |

---

### 8. THERAPY_TEMPLATES Table
**Purpose**: Reusable therapy procedure templates

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| name | VARCHAR(100) | |
| description | TEXT | |
| category | VARCHAR(50) | Panchakarma/Massage/etc. |
| duration_minutes | INTEGER | |
| preparation_steps | JSON | |
| procedure_steps | JSON | |
| post_care_instructions | JSON | |
| contraindications | JSON | |
| required_materials | JSON | |
| benefits | JSON | |
| suitable_conditions | JSON | |
| cost_range | VARCHAR(50) | |
| is_active | BOOLEAN | |

---

### 9. NOTIFICATIONS Table
**Purpose**: User notifications and alerts

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users.id |
| title | VARCHAR(255) | |
| message | TEXT | |
| type | VARCHAR(50) | appointment/reminder/system/alert |
| priority | VARCHAR(20) | low/normal/high/urgent |
| is_read | BOOLEAN | DEFAULT FALSE |
| action_url | VARCHAR(500) | |
| expires_at | DATETIME | |

---

### 10. SYSTEM_SETTINGS Table
**Purpose**: Application configuration

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| key | VARCHAR(100) | UNIQUE |
| value | JSON | |
| description | TEXT | |
| category | VARCHAR(50) | |
| is_public | BOOLEAN | Can frontend access? |
| updated_by | INTEGER | FOREIGN KEY → users.id |

---

### 11. AUDIT_LOGS Table
**Purpose**: Activity tracking and security

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users.id |
| action | VARCHAR(100) | |
| resource_type | VARCHAR(50) | |
| resource_id | INTEGER | |
| details | JSON | |
| ip_address | VARCHAR(45) | |
| user_agent | TEXT | |
| created_at | DATETIME | |

---

## Database Relationships

```
users (1) ──→ (1) patients
users (1) ──→ (1) practitioners  
users (1) ──→ (1) admins

patients (1) ──→ (∞) appointments
practitioners (1) ──→ (∞) appointments

appointments (1) ──→ (1) therapy_sessions
appointments (1) ──→ (1) feedback

patients (1) ──→ (∞) therapy_sessions
practitioners (1) ──→ (∞) therapy_sessions

patients (1) ──→ (∞) feedback
practitioners (1) ──→ (∞) feedback

users (1) ──→ (∞) notifications
```

---

## Current Database State

**Status**: ✅ Fully initialized and ready

- All 11 tables created successfully
- Schema matches backend API perfectly
- **0 users** - Fresh database
- **0 appointments** - No bookings yet
- **0 feedback** - No reviews yet

**Ready for**: User registration, authentication, and all app features!

---

## Next Steps

When the frontend connects:
1. **User Registration** → Creates entry in `users` + role-specific table
2. **Login** → Authenticates against `users`, returns JWT
3. **Appointments** → Creates entries in `appointments`
4. **Sessions** → Records in `therapy_sessions`
5. **Feedback** → Stores in `feedback`

The database will populate automatically as users interact with the application!
