import pandas as pd
import matplotlib.pyplot as plt
import os

def plot():
    if not os.path.exists("experiment_results.csv"):
        return

    try:
        df = pd.read_csv("experiment_results.csv", header=None)
    except Exception:
        return
        
    if df.shape[1] != 4:
        return

    df.columns = ["N", "BlockSize", "Time", "Perf"]
    
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    plt.subplots_adjust(hspace=0.3, wspace=0.2)

    blocks = sorted(df["BlockSize"].unique())

    for b in blocks:
        dfb = df[df["BlockSize"] == b].sort_values("N")
        axs[0, 0].plot(dfb["N"], dfb["Time"], marker='o', linewidth=2, label=f"{b}x{b} block")
    
    axs[0, 0].set_title("GPU Execution Time vs Matrix Size", fontsize=14, fontweight='bold')
    axs[0, 0].set_xlabel("Matrix Size (N)")
    axs[0, 0].set_ylabel("Time (seconds)")
    axs[0, 0].legend()
    axs[0, 0].grid(True, linestyle='--', alpha=0.7)

    for b in blocks:
        dfb = df[df["BlockSize"] == b].sort_values("N")
        axs[0, 1].plot(dfb["N"], dfb["Perf"], marker='s', linewidth=2, label=f"{b}x{b} block")
    
    axs[0, 1].set_title("GPU Performance (GFLOP/s) vs Matrix Size", fontsize=14, fontweight='bold')
    axs[0, 1].set_xlabel("Matrix Size (N)")
    axs[0, 1].set_ylabel("GFLOP/s")
    axs[0, 1].legend()
    axs[0, 1].grid(True, linestyle='--', alpha=0.7)

    max_n = df["N"].max()
    df_max = df[df["N"] == max_n].sort_values("BlockSize")

    if not df_max.empty:
        axs[1, 0].bar(df_max["BlockSize"].astype(str) + "x" + df_max["BlockSize"].astype(str), df_max["Time"], color='blue', alpha=0.7)
        for i, val in enumerate(df_max["Time"]):
            axs[1, 0].text(i, val, f"{val:.4f}", ha='center', va='bottom', fontweight='bold')
        axs[1, 0].set_title(f"Execution Time by Block Size (N={max_n})", fontsize=14, fontweight='bold')
        axs[1, 0].set_xlabel("Block Size")
        axs[1, 0].set_ylabel("Time (seconds)")
        axs[1, 0].grid(axis='y', linestyle='--', alpha=0.7)

        axs[1, 1].bar(df_max["BlockSize"].astype(str) + "x" + df_max["BlockSize"].astype(str), df_max["Perf"], color='green', alpha=0.7)
        for i, val in enumerate(df_max["Perf"]):
            axs[1, 1].text(i, val, f"{val:.1f}", ha='center', va='bottom', fontweight='bold')
        axs[1, 1].set_title(f"Performance by Block Size (N={max_n})", fontsize=14, fontweight='bold')
        axs[1, 1].set_xlabel("Block Size")
        axs[1, 1].set_ylabel("GFLOP/s")
        axs[1, 1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig("data/full_results_plot.png", dpi=150, bbox_inches='tight')

if __name__ == "__main__":
    plot()