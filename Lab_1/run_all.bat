@echo off
setlocal enabledelayedexpansion

echo [1/4] Compiling...
g++ matrix_mult.cpp -o matrix_mult.exe -O2

echo [2/4] Cleaning old data...
if exist experiment_results.csv del experiment_results.csv

echo [3/4] Running experiments (200, 400, 800, 1200, 1600, 2000)...
for %%N in (200 400 800 1200 1600 2000) do (
    echo   - Processing N=%%N...
    python generate_matrices.py %%N > nul
    matrix_mult.exe
)

echo [4/4] Generating plots...
python plot_results.py

echo All done! Check 'experiment_results.csv' and 'data/results_plot.png'
pause