@echo off
REM === Automated Python Script Runner: venv or conda ===

REM ======== CONFIGURATION (EDIT THESE PATHS) ========

REM -- Path to venv (virtual environment) folder (if using venv)
set VENV_PATH=R:\Conda VE-Internships\prodigal_env\venv

REM -- Path to conda activate.bat (if using conda)
set CONDA_ACTIVATE=R:\Conda VE-Internships\prodigal_env\Scripts\activate.bat

REM -- Name of your conda environment
set CONDA_ENV_NAME=prodigal_env

REM -- Path to your Python script (edit this for your use case)
set SCRIPT_PATH=R:\Conda VE-Internships\prodigal_env\my_script.py

REM ======== DO NOT EDIT BELOW THIS LINE UNLESS NEEDED ========

REM -- Try venv first
if exist "%VENV_PATH%\Scripts\python.exe" (
    echo [INFO] Running with Python venv...
    "%VENV_PATH%\Scripts\python.exe" "%SCRIPT_PATH%"
    goto end
)

REM -- Try conda
if exist "%CONDA_ACTIVATE%" (
    echo [INFO] Running with conda environment...
    CALL "%CONDA_ACTIVATE%" %CONDA_ENV_NAME%
    python "%SCRIPT_PATH%"
    goto end
)

REM -- Neither found
echo [ERROR] No valid venv or conda environment detected! Check your paths.

:end
pause