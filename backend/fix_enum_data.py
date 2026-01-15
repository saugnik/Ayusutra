from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./ayursutra.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fix_enums():
    db = SessionLocal()
    try:
        # Check current values
        result = db.execute(text("SELECT id, status FROM appointments WHERE status = 'scheduled'"))
        rows = result.fetchall()
        print(f"Found {len(rows)} appointments with 'scheduled' status.")

        if rows:
            print("Updating to 'SCHEDULED'...")
            db.execute(text("UPDATE appointments SET status = 'SCHEDULED' WHERE status = 'scheduled'"))
            db.commit()
            print("Update complete.")
        else:
            print("No lowercase 'scheduled' appointments found.")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_enums()
