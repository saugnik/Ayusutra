
import sys
import os
from sqlalchemy import create_engine, text

# Setup DB connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./ayursutra.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

print("Normalizing user roles to UPPERCASE in database...")

with engine.connect() as conn:
    # 1. Check before
    print("Before update:")
    result = conn.execute(text("SELECT DISTINCT role FROM users")).fetchall()
    print(result)

    # 2. Update to uppercase
    # SQLite has UPPER() function
    conn.execute(text("UPDATE users SET role = UPPER(role)"))
    conn.commit()
    print("Update executed.")

    # 3. Check after
    print("After update:")
    result = conn.execute(text("SELECT DISTINCT role FROM users")).fetchall()
    print(result)
    
print("Done.")
