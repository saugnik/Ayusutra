
import sys
import os
import io

# Redirect stdout/stderr to file
log_file = open("repro_output.txt", "w")
sys.stdout = log_file
sys.stderr = log_file

try:
    from sqlalchemy import create_engine, select, text
    from sqlalchemy.orm import sessionmaker
    import sqlalchemy

    # Add current directory to path
    sys.path.append(os.getcwd())

    from models import User, UserRole
    from database import Base
    from auth import verify_password, create_access_token

    print(f"SQLAlchemy version: {sqlalchemy.__version__}")

    # Setup DB connection
    SQLALCHEMY_DATABASE_URL = "sqlite:///./ayursutra.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    print("Database connected.")

    # 1. Raw SQL check of roles
    print("\n--- Raw SQL Check ---")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT email, role FROM users LIMIT 5"))
        for row in result:
            print(f"Email: {row[0]}, Raw Role: '{row[1]}'")

    # 2. ORM Check
    print("\n--- ORM Check ---")
    try:
        users = db.query(User).all()
        for u in users:
            print(f"ID: {u.id}, Email: {u.email}")
            print(f"  Role raw: {u.role}")
            print(f"  Role type: {type(u.role)}")
            try:
                print(f"  Role value: {u.role.value}")
            except Exception as e:
                print(f"  ERROR accessing .value: {e}")
            
    except Exception as e:
        print(f"\nCRITICAL ORM ERROR: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"Script crashed: {e}")
    import traceback
    traceback.print_exc()
finally:
    log_file.close()
