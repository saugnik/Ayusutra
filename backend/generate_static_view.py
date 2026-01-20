
import sqlite3
import json
import os
from datetime import datetime

def generate_static_view():
    print("Generating static database viewer...")
    
    db_path = "backend/ayursutra.db" if os.path.exists("backend/ayursutra.db") else "ayursutra.db"
    print(f"Connecting to: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Gather stats
    stats = {}
    tables = ["users", "patients", "practitioners", "admins", "appointments", "therapy_sessions"]
    for t in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            stats[t] = cursor.fetchone()[0]
        except:
            stats[t] = 0
            
    # 2. Gather users
    cursor.execute("SELECT id, full_name, email, role, last_login, is_active FROM users")
    users = []
    for row in cursor.fetchall():
        users.append({
            "id": row[0],
            "full_name": row[1],
            "email": row[2],
            "role": row[3],
            "last_login": row[4] or "Never",
            "is_active": bool(row[5])
        })
        
    data = {
        "stats": stats,
        "users": users
    }
    
    # 3. Read template
    with open("backend/database_viewer.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    # 4. Inject data
    # We replace the fetch logic or inject data variable
    injection = f"""
    <script>
        const STATIC_DATA = {json.dumps(data)};
        
        // Override fetch to return static data
        window.originalFetch = window.fetch;
        window.fetch = async (url) => {{
            if (url === '/debug/db-data') {{
                return {{
                    json: async () => STATIC_DATA
                }};
            }}
            return window.originalFetch(url);
        }};
    </script>
    """
    
    # Insert before </head>
    final_html = html.replace("</head>", injection + "\n</head>")
    
    output_path = os.path.abspath("backend/latest_db_view.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"Static view generated at: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_static_view()
