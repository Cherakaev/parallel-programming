@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" > nul 2>&1

set EXPERIMENT_SIZES=200 400 800 1200 1600 2000
set BLOCK_SIZES=8 16 32

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
echo [2/4] Cleaning old data...
echo ========================================
if exist experiment_results.csv del experiment_results.csv

echo ========================================
echo [3/4] Running experiments...
echo ========================================
for %%N in (%EXPERIMENT_SIZES%) do (
    echo.
    echo ----------------------------------------
    echo   --- Generating Matrices N=%%N ---
    echo ----------------------------------------
    python generate_matrices.py %%N > nul

    for %%B in (%BLOCK_SIZES%) do (
        echo   - Running N=%%N with Block Size %%Bx%%B...
        matrix_mult.exe %%B
        python verify.py
    )
)

echo.
echo ========================================
echo [4/4] Generating plots...
echo ========================================
python plot_results.py

echo.
echo All done! Check 'experiment_results.csv' and 'data/results_plot.png'
pause