@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

set MATRIX_SIZE=400
set PROCESSES=4

echo ========================================
echo [1/4] Compiling C++ code with MPI...
echo ========================================
g++ matrix_mult.cpp -o matrix_mult.exe -O2 -I"%MSMPI_INC%." -L"%MSMPI_LIB64%." -lmsmpi

if %errorlevel% neq 0 (
    exit /b
)

echo ========================================
echo [2/4] Generating test matrices N=%MATRIX_SIZE%
echo ========================================
python generate_matrices.py %MATRIX_SIZE% > nul

echo ========================================
echo [3/4] Running MPI matrix multiplication...
echo ========================================
mpiexec -n %PROCESSES% matrix_mult.exe

echo ========================================
echo [4/4] Verifying results...
echo ========================================
python verify.py

echo ========================================
echo DONE!
echo ========================================
pause