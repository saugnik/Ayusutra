
import sys
import os
sys.path.append(os.getcwd()) # Add root
try:
    from backend import main
    print("Main imported successfully")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
