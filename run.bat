@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ==========================================
:: НАСТРОЙКИ
:: ==========================================
set MATRIX_SIZE=400
set THREADS=4
:: ==========================================

echo ========================================
echo STEP 1: Compiling C++ code with OpenMP...
echo ========================================
g++ matrix_mult.cpp -o matrix_mult.exe -O2 -fopenmp

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed!
    pause
    exit /b
)

echo ========================================
echo STEP 2: Generating test matrices (N=%MATRIX_SIZE%)...
echo ========================================
python generate_matrices.py %MATRIX_SIZE%

echo ========================================
echo STEP 3: Running matrix multiplication on %THREADS% threads...
echo ========================================
matrix_mult.exe %THREADS%

echo ========================================
echo STEP 4: Verifying results...
echo ========================================
python verify.py

echo ========================================
echo DONE!
echo ========================================
pause