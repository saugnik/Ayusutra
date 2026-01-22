
import sqlite3

def find_patient():
    try:
        conn = sqlite3.connect('ayursutra.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.email, u.hashed_password 
            FROM users u 
            JOIN patients p ON u.id = p.user_id 
            LIMIT 1
        """)
        
        patient = cursor.fetchone()
        
        if patient:
            print(f"Found patient: {patient[0]}")
            # print(f"Hash: {patient[1]}") 
        else:
            print("No patients found.")
            
        conn.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    find_patient()
