"""
Debug script to check why dashboard shows 0 users
"""
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Connect to database
DATABASE_URL = "sqlite:///./ayursutra.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("=" * 60)
print("DATABASE INVESTIGATION")
print("=" * 60)

# Test 1: Check total users with raw SQL
result = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
print(f"\n1. Total users (raw SQL): {result}")

# Test 2: Check users by role (raw SQL)
print("\n2. Users by role (raw SQL):")
roles = db.execute(text("SELECT role, COUNT(*) FROM users GROUP BY role")).fetchall()
for role, count in roles:
    print(f"   - {role}: {count}")

# Test 3: Check if role values are lowercase or uppercase
print("\n3. Sample user roles:")
sample_users = db.execute(text("SELECT id, email, role FROM users LIMIT 5")).fetchall()
for user_id, email, role in sample_users:
    print(f"   - ID {user_id}: {email} -> role='{role}' (type: {type(role).__name__})")

# Test 4: Check practitioners table
try:
    pract_count = db.execute(text("SELECT COUNT(*) FROM practitioners")).scalar()
    print(f"\n4. Total practitioners in practitioners table: {pract_count}")
except Exception as e:
    print(f"\n4. Error querying practitioners: {e}")

# Test 5: Check patients table  
try:
    patient_count = db.execute(text("SELECT COUNT(*) FROM patients")).scalar()
    print(f"\n5. Total patients in patients table: {patient_count}")
except Exception as e:
    print(f"\n5. Error querying patients: {e}")

# Test 6: Check appointments
try:
    appt_count = db.execute(text("SELECT COUNT(*) FROM appointments")).scalar()
    print(f"\n6. Total appointments: {appt_count}")
except Exception as e:
    print(f"\n6. Error querying appointments: {e}")

# Test 7: Check admin users specifically
print("\n7. Admin users:")
admin_users = db.execute(text("SELECT id, email, role FROM users WHERE role LIKE '%admin%'")).fetchall()
if admin_users:
    for user_id, email, role in admin_users:
        print(f"   - ID {user_id}: {email} -> role='{role}'")
else:
    print("   - No admin users found!")

# Test 8: Check case-sensitive role matching
print("\n8. Role matching tests:")
uppercase_admin = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'ADMIN'")).scalar()
lowercase_admin = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'admin'")).scalar()
print(f"   - Uppercase 'ADMIN': {uppercase_admin}")
print(f"   - Lowercase 'admin': {lowercase_admin}")

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("=" * 60)

if result == 0:
    print("❌ Database is EMPTY - no users at all!")
elif lowercase_admin > 0 and uppercase_admin == 0:
    print("⚠️  FOUND THE ISSUE: Roles are stored as LOWERCASE in database")
    print("   but code expects UPPERCASE enum values!")
    print("\n   Solution: Update role values in database to uppercase")
elif result > 0:
    print(f"✅ Database has {result} users")
    print("   Issue might be with ORM queries or authentication")

db.close()
