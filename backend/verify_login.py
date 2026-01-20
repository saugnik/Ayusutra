
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_admin_login():
    try:
        conn = sqlite3.connect('ayursutra.db')
        cursor = conn.cursor()
        
        email = "admin_demo@test.com"
        password = "admin123"
        
        cursor.execute("SELECT hashed_password, role, is_active FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        
        if not result:
            print("User not found!")
            return
            
        stored_hash, role, is_active = result
        
        print(f"User found: {email}")
        print(f"Role: {role}")
        print(f"Active: {is_active}")
        
        if pwd_context.verify(password, stored_hash):
            print("Password verification: SUCCESS")
        else:
            print("Password verification: FAILED")
            print(f"Hash in DB: {stored_hash}")
            new_hash = pwd_context.hash(password)
            print(f"Expected hash for '{password}': {new_hash}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_admin_login()
