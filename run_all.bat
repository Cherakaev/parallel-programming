@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

set EXPERIMENT_SIZES=200 400 800 1200 1600 2000
set THREADS_LIST=1 2 4 8 12

echo ========================================
echo [1/4] Compiling with OpenMP...
echo ========================================
g++ matrix_mult.cpp -o matrix_mult.exe -O2 -fopenmp

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
    
    for %%T in (%THREADS_LIST%) do (
        echo   - Running N=%%N with %%T threads...
        matrix_mult.exe %%T
        
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