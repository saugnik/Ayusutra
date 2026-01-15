import os
from fastapi.responses import HTMLResponse, JSONResponse

try:
    path = os.path.dirname(os.path.abspath(__file__))
    print(f"Path: {path}")
    resp = HTMLResponse(content="<h1>Test</h1>")
    print("HTMLResponse created successfully")
except Exception as e:
    print(f"Error: {e}")
