@echo off
REM Setup script for GitHub Issue Assistant (Windows)

echo 🚀 Setting up GitHub Issue Assistant...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your OPENAI_API_KEY
) else (
    echo ✅ .env file already exists
)

echo.
echo ✨ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your OPENAI_API_KEY
echo 2. Run backend: cd backend ^&^& python -m uvicorn main:app --reload
echo 3. Run frontend: streamlit run frontend/app.py
echo.
pause
