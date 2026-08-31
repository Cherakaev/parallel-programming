@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" > nul 2>&1

set MATRIX_SIZE=800
set BLOCK_SIZE=16

echo ========================================
echo [1/4] Compiling CUDA code...
echo ========================================
nvcc matrix_mult.cu -o matrix_mult.exe -O2

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed!
    pause
    exit /b
)

echo ========================================
echo [2/4] Generating test matrices N=%MATRIX_SIZE%
echo ========================================
python generate_matrices.py %MATRIX_SIZE% > nul

echo ========================================
echo [3/4] Running CUDA matrix multiplication...
echo ========================================
matrix_mult.exe %BLOCK_SIZE%

echo ========================================
echo [4/4] Verifying results...
echo ========================================
python verify.py

echo ========================================
echo DONE!
echo ========================================
pause
