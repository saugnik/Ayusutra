import sqlite3

conn = sqlite3.connect('ayursutra.db')
cursor = conn.cursor()

# Get all users
cursor.execute("""
    SELECT id, email, full_name, role, is_active, created_at, updated_at
    FROM users
    ORDER BY created_at DESC
""")

users = cursor.fetchall()

output = []
output.append("=" * 100)
output.append("ALL LOGIN DATA - AYURSUTRA DATABASE")
output.append("=" * 100)
output.append(f"\nTotal Users: {len(users)}\n")

for i, user in enumerate(users, 1):
    user_id, email, full_name, role, is_active, created_at, updated_at = user
    
    output.append("-" * 100)
    output.append(f"USER #{i}")
    output.append(f"ID: {user_id}")
    output.append(f"Email: {email}")
    output.append(f"Name: {full_name}")
    output.append(f"Role: {role}")
    output.append(f"Active: {'Yes' if is_active else 'No'}")
    output.append(f"Created: {created_at}")
    output.append(f"Updated: {updated_at}")
    
    # Get role-specific details
    if role == 'patient':
        cursor.execute("SELECT phone, date_of_birth, gender FROM patients WHERE user_id = ?", (user_id,))
        patient = cursor.fetchone()
        if patient:
            output.append(f"Phone: {patient[0] or 'N/A'}")
            output.append(f"DOB: {patient[1] or 'N/A'}")
            output.append(f"Gender: {patient[2] or 'N/A'}")
    
    elif role == 'practitioner':
        cursor.execute("SELECT specialization, license_number, phone FROM practitioners WHERE user_id = ?", (user_id,))
        prac = cursor.fetchone()
        if prac:
            output.append(f"Specialization: {prac[0] or 'N/A'}")
            output.append(f"License: {prac[1] or 'N/A'}")
            output.append(f"Phone: {prac[2] or 'N/A'}")
    
    output.append("")

# Statistics
output.append("=" * 100)
output.append("STATISTICS")
output.append("=" * 100)
cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'patient'")
patients = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'practitioner'")
practitioners = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
admins = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
active = cursor.fetchone()[0]

output.append(f"Total: {len(users)}")
output.append(f"Patients: {patients}")
output.append(f"Practitioners: {practitioners}")
output.append(f"Admins: {admins}")
output.append(f"Active: {active}")
output.append(f"Inactive: {len(users) - active}")
output.append("=" * 100)

# Write to file
with open('all_login_data.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"Login data exported to: all_login_data.txt")
print(f"Total users: {len(users)}")

conn.close()
