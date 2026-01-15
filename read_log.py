try:
    with open("backend/server_log.txt", "r", encoding="utf-16") as f:
        print(f.read())
except Exception as e: # Try utf-8 if utf-16 fails
    try:
        with open("backend/server_log.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e2:
        print(f"Failed to read: {e}, {e2}")
