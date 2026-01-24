"""
Database Cleanup Script - Remove Fake/Test Data
================================================
This script removes fake clinics and associated test data from the database.

SAFETY FEATURES:
- Dry-run mode by default (preview changes without executing)
- Explicit confirmation required for actual deletion
- Detailed logging of all operations
- Rollback on error

Usage:
    python cleanup_fake_data.py --dry-run    # Preview changes (default)
    python cleanup_fake_data.py --execute    # Actually delete data
"""

import argparse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Practitioner, Patient, Appointment, PatientHealthLog, UserRole
from datetime import datetime

# List of fake clinic names to remove
FAKE_CLINICS = [
    "AyurHealth Clinic",
    "www.wewantit.com",
    "newnew",
    "new",
    "Default Clinic",
    "AyurSutra Wellness Center",
    "Various Locations"  # Generic test location
]

def cleanup_fake_data(dry_run=True):
    """
    Remove fake clinic data from the database.
    
    Args:
        dry_run (bool): If True, only preview changes without executing
    """
    db: Session = SessionLocal()
    
    try:
        print("=" * 60)
        print("DATABASE CLEANUP - FAKE DATA REMOVAL")
        print("=" * 60)
        print(f"Mode: {'DRY RUN (Preview Only)' if dry_run else 'EXECUTE (Actual Deletion)'}")
        print(f"Timestamp: {datetime.now()}")
        print("=" * 60)
        print()
        
        # Find all practitioners with fake clinic names
        fake_practitioners = db.query(Practitioner).join(User).filter(
            Practitioner.clinic_name.in_(FAKE_CLINICS)
        ).all()
        
        print(f"📊 Found {len(fake_practitioners)} practitioners with fake clinic names:")
        print()
        
        total_appointments = 0
        total_health_logs = 0
        total_patients = 0
        
        for prac in fake_practitioners:
            user = db.query(User).filter(User.id == prac.user_id).first()
            print(f"  👨‍⚕️ Practitioner: {user.full_name if user else 'Unknown'}")
            print(f"     Email: {user.email if user else 'Unknown'}")
            print(f"     Clinic: {prac.clinic_name}")
            print(f"     License: {prac.license_number}")
            
            # Count associated appointments
            appointments = db.query(Appointment).filter(
                Appointment.practitioner_id == prac.id
            ).all()
            print(f"     Appointments: {len(appointments)}")
            total_appointments += len(appointments)
            
            # Count associated health logs
            health_logs = db.query(PatientHealthLog).filter(
                PatientHealthLog.practitioner_id == prac.id
            ).all()
            print(f"     Health Logs: {len(health_logs)}")
            total_health_logs += len(health_logs)
            
            print()
        
        # Find test patients (demo accounts)
        test_patient_emails = [
            "patient_demo@test.com",
            "demo@test.com",
            "test@test.com"
        ]
        
        test_patients = db.query(Patient).join(User).filter(
            User.email.in_(test_patient_emails)
        ).all()
        
        print(f"📊 Found {len(test_patients)} test patient accounts:")
        print()
        
        for patient in test_patients:
            user = db.query(User).filter(User.id == patient.user_id).first()
            print(f"  👤 Patient: {user.full_name if user else 'Unknown'}")
            print(f"     Email: {user.email if user else 'Unknown'}")
            
            # Count associated appointments
            appointments = db.query(Appointment).filter(
                Appointment.patient_id == patient.id
            ).all()
            print(f"     Appointments: {len(appointments)}")
            
            # Count associated health logs
            health_logs = db.query(PatientHealthLog).filter(
                PatientHealthLog.patient_id == patient.id
            ).all()
            print(f"     Health Logs: {len(health_logs)}")
            print()
        
        total_patients = len(test_patients)
        
        # Summary
        print("=" * 60)
        print("SUMMARY OF CHANGES")
        print("=" * 60)
        print(f"Practitioners to delete: {len(fake_practitioners)}")
        print(f"Test patients to delete: {total_patients}")
        print(f"Appointments to delete: {total_appointments}")
        print(f"Health logs to delete: {total_health_logs}")
        print(f"Total users to delete: {len(fake_practitioners) + total_patients}")
        print("=" * 60)
        print()
        
        if dry_run:
            print("✅ DRY RUN COMPLETE - No data was deleted")
            print("   Run with --execute flag to actually delete this data")
        else:
            # Confirm deletion
            print("⚠️  WARNING: This will permanently delete the data listed above!")
            confirm = input("Type 'DELETE' to confirm: ")
            
            if confirm != "DELETE":
                print("❌ Deletion cancelled")
                return
            
            print()
            print("🗑️  Deleting data...")
            print()
            
            # Delete in correct order (foreign key constraints)
            deleted_count = 0
            
            # 1. Delete appointments
            for prac in fake_practitioners:
                appointments = db.query(Appointment).filter(
                    Appointment.practitioner_id == prac.id
                ).all()
                for appt in appointments:
                    db.delete(appt)
                    deleted_count += 1
            
            for patient in test_patients:
                appointments = db.query(Appointment).filter(
                    Appointment.patient_id == patient.id
                ).all()
                for appt in appointments:
                    db.delete(appt)
                    deleted_count += 1
            
            print(f"   ✓ Deleted {deleted_count} appointments")
            
            # 2. Delete health logs
            deleted_count = 0
            for prac in fake_practitioners:
                logs = db.query(PatientHealthLog).filter(
                    PatientHealthLog.practitioner_id == prac.id
                ).all()
                for log in logs:
                    db.delete(log)
                    deleted_count += 1
            
            for patient in test_patients:
                logs = db.query(PatientHealthLog).filter(
                    PatientHealthLog.patient_id == patient.id
                ).all()
                for log in logs:
                    db.delete(log)
                    deleted_count += 1
            
            print(f"   ✓ Deleted {deleted_count} health logs")
            
            # 3. Delete patient profiles
            deleted_count = 0
            for patient in test_patients:
                db.delete(patient)
                deleted_count += 1
            print(f"   ✓ Deleted {deleted_count} patient profiles")
            
            # 4. Delete practitioner profiles
            deleted_count = 0
            for prac in fake_practitioners:
                db.delete(prac)
                deleted_count += 1
            print(f"   ✓ Deleted {deleted_count} practitioner profiles")
            
            # 5. Delete user accounts
            deleted_count = 0
            for prac in fake_practitioners:
                user = db.query(User).filter(User.id == prac.user_id).first()
                if user:
                    db.delete(user)
                    deleted_count += 1
            
            for patient in test_patients:
                user = db.query(User).filter(User.id == patient.user_id).first()
                if user:
                    db.delete(user)
                    deleted_count += 1
            
            print(f"   ✓ Deleted {deleted_count} user accounts")
            print()
            
            # Commit changes
            db.commit()
            
            print("=" * 60)
            print("✅ CLEANUP COMPLETE - All fake data has been removed")
            print("=" * 60)
    
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR OCCURRED")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Rolling back changes...")
        db.rollback()
        print("✅ Rollback complete - No data was modified")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(
        description="Clean up fake/test data from the database"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete data (default is dry-run)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Preview changes without deleting (default)"
    )
    
    args = parser.parse_args()
    
    # If --execute is specified, set dry_run to False
    dry_run = not args.execute
    
    cleanup_fake_data(dry_run=dry_run)

if __name__ == "__main__":
    main()
