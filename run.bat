@echo off
REM ----- DjangoVibe demo launcher (Windows cmd) -----
REM Calls venv binaries directly so spawned windows don't need to re-activate.

if not exist "venv\Scripts\python.exe" (
    echo.
    echo [!] venv not found. Run setup first:
    echo     python -m venv venv
    echo     venv\Scripts\activate.bat
    echo     pip install -r requirements.txt
    echo     python manage.py migrate
    echo.
    exit /b 1
)

set ST_FLAGS=--server.headless true --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false

echo Launching Streamlit dashboard #1 on http://localhost:8501 ...
start "Streamlit Iris (8501)" cmd /k "venv\Scripts\streamlit.exe run streamlit_apps\dashboard1.py --server.port 8501 %ST_FLAGS%"

echo Launching Streamlit dashboard #2 on http://localhost:8502 ...
start "Streamlit Gapminder (8502)" cmd /k "venv\Scripts\streamlit.exe run streamlit_apps\dashboard2.py --server.port 8502 %ST_FLAGS%"

echo Launching Django on http://localhost:8000 ...
start "Django (8000)" cmd /k "venv\Scripts\python.exe manage.py runserver 8000"

echo.
echo All three servers starting up. Streamlit takes ~5-10 sec to fully initialize.
echo Open http://localhost:8000 in your browser when ready.
echo Close each terminal window to stop a server.
