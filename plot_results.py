import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def plot():
    if not os.path.exists("experiment_results.csv"):
        print("CSV not found!")
        return

    # Загружаем данные
    df = pd.read_csv("experiment_results.csv", names=["N", "Time", "Perf"])
    df = df.sort_values("N")


    df["Memory"] = (3 * df["N"] ** 2 * 8) / (1024 * 1024)


    k = df["Time"].iloc[-1] / (df["N"].iloc[-1] ** 3)
    df["Theory"] = k * (df["N"] ** 3)


    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    plt.subplots_adjust(hspace=0.3, wspace=0.2)


    axs[0, 0].plot(df["N"], df["Time"], 'o-', linewidth=2, color='blue', label='Actual Time')
    for x, y in zip(df["N"], df["Time"]):
        axs[0, 0].annotate(f'{y:.3f}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)
    axs[0, 0].set_title("Execution Time vs Matrix Size", fontsize=14, fontweight='bold')
    axs[0, 0].set_ylabel("Time (seconds)")
    axs[0, 0].grid(True, linestyle='--', alpha=0.7)


    axs[0, 1].plot(df["N"], df["Perf"], 's-', linewidth=2, color='red')

    peak_idx = df["Perf"].idxmax()
    peak_n = df.loc[peak_idx, "N"]
    peak_val = df.loc[peak_idx, "Perf"]
    axs[0, 1].annotate(f'Peak: {peak_val:.2f}', (peak_n, peak_val), xytext=(peak_n, peak_val + 0.5),
                       fontweight='bold', color='darkred', ha='center')
    axs[0, 1].set_title("Performance (GFLOP/s)", fontsize=14, fontweight='bold')
    axs[0, 1].set_ylabel("GFLOP/s")
    axs[0, 1].grid(True, linestyle='--', alpha=0.7)


    bars = axs[1, 0].bar(df["N"].astype(str), df["Memory"], color='green', alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        axs[1, 0].annotate(f'{height:.1f}', (bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    axs[1, 0].set_title("Memory Consumption (MB)", fontsize=14, fontweight='bold')
    axs[1, 0].set_ylabel("MB (3 matrices x N^2 x double)")
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.7)


    axs[1, 1].plot(df["N"], df["Time"], 'o-', label='Actual', color='blue')
    axs[1, 1].plot(df["N"], df["Theory"], '--', label='Theoretical O(N^3)', color='purple', alpha=0.6)
    axs[1, 1].set_title("Comparison with O(N^3) complexity", fontsize=14, fontweight='bold')
    axs[1, 1].legend()
    axs[1, 1].grid(True, linestyle='--', alpha=0.7)


    for ax in axs.flat:
        ax.set_xlabel("Matrix Size (N)")

    plt.savefig("data/full_results_plot.png", dpi=150, bbox_inches='tight')
    print("All 4 plots saved to data/full_results_plot.png")


if __name__ == "__main__":
    plot()