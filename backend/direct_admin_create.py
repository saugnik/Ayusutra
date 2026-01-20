
import sqlite3
from auth import get_password_hash
from datetime import datetime
import json

def create_admin_direct():
    DB_FILE = "ayursutra.db"
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        email = "admin_demo@test.com"
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()
        
        if existing:
             print(f"Admin user already exists. ID: {existing[0]}")
             # Ensure admin profile exists
             cursor.execute("SELECT id FROM admins WHERE user_id = ?", (existing[0],))
             admin_prof = cursor.fetchone()
             if not admin_prof:
                 print("Creating missing admin profile...")
                 cursor.execute("""
                    INSERT INTO admins (user_id, admin_level, permissions, department, created_at)
                    VALUES (?, ?, ?, ?, ?)
                 """, (existing[0], "super", json.dumps(["all"]), "IT", datetime.now()))
                 conn.commit()
                 print("Admin profile created.")
        else:
            print(f"Creating new admin user: {email}")
            hashed_pw = get_password_hash("admin123")
            
            # Insert User
            cursor.execute("""
                INSERT INTO users (email, full_name, hashed_password, role, is_active, is_verified, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (email, "System Admin", hashed_pw, "admin", 1, 1, datetime.now()))
            
            user_id = cursor.lastrowid
            
            # Insert Admin Profile
            cursor.execute("""
                INSERT INTO admins (user_id, admin_level, permissions, department, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, "super", json.dumps(["all"]), "IT", datetime.now()))
            
            conn.commit()
            print("Admin user created successfully.")
            
        print(f"\nAdmin Credentials:\nEmail: {email}\nPassword: admin123")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    create_admin_direct()
