import sqlite3
import sys

def view_users():
    db_path = "ayursutra.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    output = []
    output.append("\n" + "="*85)
    output.append(f"{'ID':<4} | {'ROLE':<12} | {'EMAIL':<35} | {'LAST LOGIN'}")
    output.append("="*85)
    
    try:
        # Get users with last_login
        cursor.execute("SELECT id, role, email, last_login FROM users ORDER BY id")
        users = cursor.fetchall()
        
        if not users:
            output.append("No users found in database.")
        
        for user in users:
            uid = str(user[0])
            role = str(user[1]) if user[1] else "None"
            # Clean up role format
            if "UserRole." in role:
                role = role.replace("UserRole.", "")
            
            email = str(user[2])
            last_login = str(user[3]) if user[3] else "Never"
            
            output.append(f"{uid:<4} | {role:<12} | {email:<35} | {last_login}")
            
    except sqlite3.Error as e:
        output.append(f"Database error: {e}")
    finally:
        output.append("="*85 + "\n")
        conn.close()
        
    # Write to file
    with open("users_export.txt", "w") as f:
        f.write("\n".join(output))
    
    # Also print to stdout
    print("\n".join(output))

if __name__ == "__main__":
    view_users()
