
import sqlite3
import os

def delete_practitioner():
    db_path = "backend/ayursutra.db"
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get user_id for the practitioner with license 236512
        cursor.execute("SELECT user_id FROM practitioners WHERE license_number = ?", ('236512',))
        row = cursor.fetchone()
        
        if row:
            user_id = row[0]
            print(f"Found conflicting practitioner. User ID: {user_id}")
            
            # Delete from practitioners
            cursor.execute("DELETE FROM practitioners WHERE license_number = ?", ('236512',))
            print("Deleted from practitioners table.")
            
            # Delete from users
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            print(f"Deleted user {user_id} from users table.")
            
            conn.commit()
            print("Successfully removed conflicting user.")
        else:
            print("No practitioner found with license '236512'.")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    delete_practitioner()
