
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Importing schemas...")
try:
    import schemas
    print("Schemas imported successfully.")
except Exception as e:
    print(f"Error importing schemas: {e}")
    import traceback
    traceback.print_exc()
