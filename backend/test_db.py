
from database import SessionLocal
from sqlalchemy import text

def test_db():
    print("Testing DB Connection...")
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        print(f"Success! Result: {result.fetchone()}")
        db.close()
    except Exception as e:
        print("DB Connection Failed!")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_db()
