from sqlalchemy import create_engine, text
from backend.database import DATABASE_URL

def add_geo_columns():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Adding latitude column...")
        try:
            conn.execute(text("ALTER TABLE practitioners ADD COLUMN latitude FLOAT"))
        except Exception as e:
            print(f"Skipping latitude (maybe exists): {e}")

        print("Adding longitude column...")
        try:
            conn.execute(text("ALTER TABLE practitioners ADD COLUMN longitude FLOAT"))
        except Exception as e:
            print(f"Skipping longitude (maybe exists): {e}")
            
        print("Done.")

if __name__ == "__main__":
    add_geo_columns()
