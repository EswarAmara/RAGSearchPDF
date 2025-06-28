@echo off
REM RAG Streamlit Application Deployment Script for Windows

echo 🚀 Starting RAG Streamlit Application Deployment...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose found

REM Create uploads directory if it doesn't exist
if not exist "uploads" mkdir uploads

REM Build and start the application
echo 🔨 Building and starting the application...
docker-compose up --build -d

REM Wait for the application to start
echo ⏳ Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Check if the application is running
curl -f http://localhost:8501/_stcore/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Application failed to start. Check logs with: docker-compose logs
    pause
    exit /b 1
) else (
    echo ✅ Application is running successfully!
    echo 🌐 Open your browser and navigate to: http://localhost:8501
    echo.
    echo 📋 Useful commands:
    echo    View logs: docker-compose logs -f
    echo    Stop app: docker-compose down
    echo    Restart app: docker-compose restart
)

pause 