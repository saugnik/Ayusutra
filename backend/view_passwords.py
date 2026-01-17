import sqlite3

conn = sqlite3.connect('ayursutra.db')
cursor = conn.cursor()

# Check if password column exists
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

print("\n" + "=" * 120)
print("USER CREDENTIALS - INCLUDING PASSWORDS")
print("=" * 120)

print("\nColumns in users table:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# Get all users with passwords
cursor.execute("""
    SELECT id, email, full_name, role, hashed_password, is_active, created_at
    FROM users
    ORDER BY created_at DESC
""")

users = cursor.fetchall()

print(f"\n\nTotal Users: {len(users)}\n")
print("=" * 120)

for i, user in enumerate(users, 1):
    user_id, email, full_name, role, hashed_password, is_active, created_at = user
    
    print(f"\nUSER #{i}")
    print("-" * 120)
    print(f"ID:                {user_id}")
    print(f"Email:             {email}")
    print(f"Name:              {full_name}")
    print(f"Role:              {role}")
    print(f"Active:            {'Yes' if is_active else 'No'}")
    print(f"Created:           {created_at}")
    print(f"Hashed Password:   {hashed_password[:80] if hashed_password else 'N/A'}...")
    
    # Get role-specific info
    if role == 'patient':
        cursor.execute("SELECT phone FROM patients WHERE user_id = ?", (user_id,))
        patient = cursor.fetchone()
        if patient:
            print(f"Phone:             {patient[0] or 'N/A'}")
    
    elif role == 'practitioner':
        cursor.execute("SELECT specialization, phone FROM practitioners WHERE user_id = ?", (user_id,))
        prac = cursor.fetchone()
        if prac:
            print(f"Specialization:    {prac[0] or 'N/A'}")
            print(f"Phone:             {prac[1] or 'N/A'}")

print("\n" + "=" * 120)
print("\nNOTE: Passwords are hashed using bcrypt for security.")
print("The actual passwords cannot be retrieved - only verified against the hash.")
print("=" * 120 + "\n")

# Export to file
with open('user_credentials.txt', 'w', encoding='utf-8') as f:
    f.write("USER CREDENTIALS WITH HASHED PASSWORDS\n")
    f.write("=" * 120 + "\n\n")
    
    for i, user in enumerate(users, 1):
        user_id, email, full_name, role, hashed_password, is_active, created_at = user
        f.write(f"\nUSER #{i}\n")
        f.write(f"ID: {user_id}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Name: {full_name}\n")
        f.write(f"Role: {role}\n")
        f.write(f"Active: {'Yes' if is_active else 'No'}\n")
        f.write(f"Created: {created_at}\n")
        f.write(f"Hashed Password: {hashed_password}\n")
        f.write("-" * 120 + "\n")

print("Credentials exported to: user_credentials.txt")

conn.close()
