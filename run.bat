@echo off
chcp 65001 > nul
echo ========================================
echo STEP 1: Compiling C++ code...
echo ========================================
g++ matrix_mult.cpp -o matrix_mult.exe -O2

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed!
    pause
    exit /b
)

echo ========================================
echo STEP 2: Generating test matrices (N=400)...
echo ========================================
python generate_matrices.py 400

echo ========================================
echo STEP 3: Running matrix multiplication...
echo ========================================
matrix_mult.exe

echo ========================================
echo STEP 4: Verifying results...
echo ========================================
python verify.py

echo ========================================
echo DONE!
echo ========================================
pause