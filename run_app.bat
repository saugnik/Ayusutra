echo off
echo ===========================================
echo      Starting AyurSutra Application
echo ===========================================

echo 1. Launching Main Backend Server...
start "AyurSutra Main Backend" cmd /k "cd backend && python main.py"

echo 2. Launching AI RAG Service...
start "AyurSutra AI Service" cmd /k "cd backend && python rag_finetune_service.py"

echo 3. Launching Frontend Application...
start "AyurSutra Frontend" cmd /k "npm start"

echo ===========================================
echo      Servers are starting up!
echo      Main Backend: http://localhost:8001
echo      AI Service:   http://localhost:8000
echo      Frontend:     http://localhost:3000
echo ===========================================
pause
