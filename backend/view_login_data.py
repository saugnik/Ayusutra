"""
View all login data from the database
"""

import sqlite3
from datetime import datetime

def view_login_data():
    conn = sqlite3.connect('ayursutra.db')
    cursor = conn.cursor()
    
    print("\n" + "=" * 120)
    print(" " * 45 + "LOGIN DATA VIEWER")
    print("=" * 120)
    
    # Get all users with their role information
    cursor.execute("""
        SELECT 
            u.id,
            u.email,
            u.full_name,
            u.role,
            u.is_active,
            u.created_at,
            u.updated_at
        FROM users u
        ORDER BY u.created_at DESC
    """)
    
    users = cursor.fetchall()
    
    print(f"\nTotal Users: {len(users)}\n")
    
    if not users:
        print("No users found in the database.")
        conn.close()
        return
    
    # Display each user
    for i, user in enumerate(users, 1):
        user_id, email, full_name, role, is_active, created_at, updated_at = user
        
        print("=" * 120)
        print(f"USER #{i}")
        print("=" * 120)
        print(f"ID:              {user_id}")
        print(f"Email:           {email}")
        print(f"Full Name:       {full_name}")
        print(f"Role:            {role}")
        print(f"Active:          {'Yes' if is_active else 'No'}")
        print(f"Created:         {created_at}")
        print(f"Last Updated:    {updated_at}")
        
        # Get role-specific data
        if role == 'patient':
            cursor.execute("""
                SELECT phone, date_of_birth, gender, address, emergency_contact
                FROM patients
                WHERE user_id = ?
            """, (user_id,))
            patient_data = cursor.fetchone()
            if patient_data:
                phone, dob, gender, address, emergency = patient_data
                print(f"\nPatient Details:")
                print(f"  Phone:            {phone or 'N/A'}")
                print(f"  Date of Birth:    {dob or 'N/A'}")
                print(f"  Gender:           {gender or 'N/A'}")
                print(f"  Address:          {address or 'N/A'}")
                print(f"  Emergency:        {emergency or 'N/A'}")
        
        elif role == 'practitioner':
            cursor.execute("""
                SELECT specialization, license_number, phone, bio, years_of_experience
                FROM practitioners
                WHERE user_id = ?
            """, (user_id,))
            prac_data = cursor.fetchone()
            if prac_data:
                spec, license, phone, bio, years = prac_data
                print(f"\nPractitioner Details:")
                print(f"  Specialization:   {spec or 'N/A'}")
                print(f"  License:          {license or 'N/A'}")
                print(f"  Phone:            {phone or 'N/A'}")
                print(f"  Experience:       {years or 'N/A'} years")
                print(f"  Bio:              {bio[:60] + '...' if bio and len(bio) > 60 else bio or 'N/A'}")
        
        elif role == 'admin':
            cursor.execute("""
                SELECT permissions, department
                FROM admins
                WHERE user_id = ?
            """, (user_id,))
            admin_data = cursor.fetchone()
            if admin_data:
                perms, dept = admin_data
                print(f"\nAdmin Details:")
                print(f"  Permissions:      {perms or 'N/A'}")
                print(f"  Department:       {dept or 'N/A'}")
        
        print()
    
    # Summary statistics
    print("=" * 120)
    print("SUMMARY STATISTICS")
    print("=" * 120)
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'patient'")
    patient_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'practitioner'")
    prac_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    admin_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
    active_count = cursor.fetchone()[0]
    
    print(f"\nTotal Users:         {len(users)}")
    print(f"Patients:            {patient_count}")
    print(f"Practitioners:       {prac_count}")
    print(f"Admins:              {admin_count}")
    print(f"Active Users:        {active_count}")
    print(f"Inactive Users:      {len(users) - active_count}")
    
    print("\n" + "=" * 120 + "\n")
    
    conn.close()

if __name__ == "__main__":
    try:
        view_login_data()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
