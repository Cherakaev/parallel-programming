@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ==========================================
:: НАСТРОЙКИ
:: ==========================================
set EXPERIMENT_SIZES=200 400 800 1200 1600 2000
:: ==========================================

echo [1/4] Compiling...
g++ matrix_mult.cpp -o matrix_mult.exe -O2

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed!
    pause
    exit /b
)

echo [2/4] Cleaning old data...
if exist experiment_results.csv del experiment_results.csv

echo [3/4] Running experiments (%EXPERIMENT_SIZES%)...
for %%N in (%EXPERIMENT_SIZES%) do (
    echo.
    echo   --- Processing N=%%N ---
    
    :: 1. Генерация
    python generate_matrices.py %%N > nul
    
    :: 2. Вычисление C++
    matrix_mult.exe
    
    :: 3. Проверка
    python verify.py
)

echo.
echo [4/4] Generating plots...
python plot_results.py

echo.
echo All done! Check 'experiment_results.csv' and 'data/results_plot.png'
pause