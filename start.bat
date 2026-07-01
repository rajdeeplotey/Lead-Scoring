@echo off
echo Starting B Socio Lead Scoring Web Application...
echo.

echo Starting Flask Backend on port 5000...
start "Flask Backend" cmd /k "cd /d %~dp0 && python web/backend/app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend on port 8080...
start "Frontend Server" cmd /k "cd /d %~dp0/web/frontend && python -m http.server 8080"

echo.
echo ========================================
echo Website is starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8080
echo ========================================
echo.
echo Press any key to open the website in your browser...
pause >nul

start http://localhost:8080

echo.
echo Website opened in browser!
echo Close this window to stop both servers (or close the individual server windows).
