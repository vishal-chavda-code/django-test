@echo off
REM ----- DjangoVibe demo launcher (Windows) -----
REM Starts the two Streamlit dashboards and the Django dev server, each in
REM its own window so you can see logs separately.

if not exist "venv\Scripts\activate.bat" (
    echo.
    echo [!] venv not found. Run setup first:
    echo     python -m venv venv
    echo     venv\Scripts\activate
    echo     pip install -r requirements.txt
    echo.
    exit /b 1
)

echo Launching Streamlit dashboard #1 on http://localhost:8501 ...
start "Streamlit Iris (8501)" cmd /k "venv\Scripts\activate && streamlit run streamlit_apps\dashboard1.py --server.port 8501"

echo Launching Streamlit dashboard #2 on http://localhost:8502 ...
start "Streamlit Gapminder (8502)" cmd /k "venv\Scripts\activate && streamlit run streamlit_apps\dashboard2.py --server.port 8502"

echo Launching Django on http://localhost:8000 ...
start "Django (8000)" cmd /k "venv\Scripts\activate && python manage.py runserver"

echo.
echo All three servers starting up. Open http://localhost:8000 in your browser.
echo Close each terminal window to stop a server.
