import pandas as pd
import matplotlib.pyplot as plt
import os

def plot():
    if not os.path.exists("experiment_results.csv"):
        print("Error: CSV file not found.")
        return

    try:
        df = pd.read_csv("experiment_results.csv", header=None)
    except Exception as e:
        print("Error reading CSV:", e)
        return
        
    if df.shape[1] != 4:
        print(f"ERROR: Expected 4 columns in CSV, but found {df.shape[1]}.")
        return

    df.columns = ["N", "Threads", "Time", "Perf"]
    
    df["Memory_MB"] = (df["Threads"] + 2) * (df["N"] ** 2) * 8 / (1024 * 1024)
    
    # Теперь сетка 3x2 для новых графиков
    fig, axs = plt.subplots(3, 2, figsize=(16, 18))
    plt.subplots_adjust(hspace=0.4, wspace=0.2)

    threads = sorted(df["Threads"].unique())

    for t in threads:
        dft = df[df["Threads"] == t].sort_values("N")
        axs[0, 0].plot(dft["N"], dft["Time"], marker='o', linewidth=2, label=f"{t} procs")
    axs[0, 0].set_title("Execution Time vs Matrix Size", fontsize=14, fontweight='bold')
    axs[0, 0].set_xlabel("Matrix Size (N)")
    axs[0, 0].set_ylabel("Time (seconds)")
    axs[0, 0].legend()
    axs[0, 0].grid(True, linestyle='--', alpha=0.7)

    for t in threads:
        dft = df[df["Threads"] == t].sort_values("N")
        axs[0, 1].plot(dft["N"], dft["Perf"], marker='s', linewidth=2, label=f"{t} procs")
    axs[0, 1].set_title("Performance (GFLOP/s) vs Matrix Size", fontsize=14, fontweight='bold')
    axs[0, 1].set_xlabel("Matrix Size (N)")
    axs[0, 1].set_ylabel("GFLOP/s")
    axs[0, 1].legend()
    axs[0, 1].grid(True, linestyle='--', alpha=0.7)

    max_n = df["N"].max()
    df_max = df[df["N"] == max_n].sort_values("Threads")

    if not df_max.empty and 1 in df_max["Threads"].values:
        t1_time = df_max[df_max["Threads"] == 1]["Time"].values[0]
        df_max["Speedup"] = t1_time / df_max["Time"]
        
        axs[1, 0].plot(df_max["Threads"], df_max["Speedup"], 'o-', color='blue', linewidth=2, label='Actual Speedup')
        axs[1, 0].plot(df_max["Threads"], df_max["Threads"], '--', color='red', alpha=0.6, label='Ideal Speedup')
        axs[1, 0].set_title(f"Speedup vs Processes (N={max_n})", fontsize=14, fontweight='bold')
        axs[1, 0].set_xlabel("Number of Processes")
        axs[1, 0].set_ylabel("Speedup (T1 / Tn)")
        axs[1, 0].set_xticks(threads)
        axs[1, 0].legend()
        axs[1, 0].grid(True, linestyle='--', alpha=0.7)

        df_max["Efficiency"] = df_max["Speedup"] / df_max["Threads"]
        
        axs[1, 1].plot(df_max["Threads"], df_max["Efficiency"], 'd-', color='green', linewidth=2, label='Efficiency')
        axs[1, 1].axhline(y=1.0, color='red', linestyle='--', alpha=0.6, label='Ideal Efficiency')
        axs[1, 1].set_title(f"Efficiency vs Processes (N={max_n})", fontsize=14, fontweight='bold')
        axs[1, 1].set_xlabel("Number of Processes")
        axs[1, 1].set_ylabel("Efficiency")
        axs[1, 1].set_xticks(threads)
        axs[1, 1].set_ylim(0, 1.1)
        axs[1, 1].legend()
        axs[1, 1].grid(True, linestyle='--', alpha=0.7)

        axs[2, 0].bar(df_max["Threads"].astype(str), df_max["Memory_MB"], color='purple', alpha=0.7)
        for i, val in enumerate(df_max["Memory_MB"]):
            axs[2, 0].text(i, val + 2, f"{val:.0f}", ha='center', fontweight='bold')
        axs[2, 0].set_title(f"Total RAM Consumed (N={max_n})", fontsize=14, fontweight='bold')
        axs[2, 0].set_xlabel("Number of Processes")
        axs[2, 0].set_ylabel("Total Memory (MB)")
        axs[2, 0].grid(axis='y', linestyle='--', alpha=0.7)

    for t in threads:
        dft = df[df["Threads"] == t].sort_values("N")
        axs[2, 1].plot(dft["N"], dft["Memory_MB"], marker='^', linewidth=2, label=f"{t} procs")
    axs[2, 1].set_title("Total RAM Consumed vs Matrix Size", fontsize=14, fontweight='bold')
    axs[2, 1].set_xlabel("Matrix Size (N)")
    axs[2, 1].set_ylabel("Total Memory (MB)")
    axs[2, 1].legend()
    axs[2, 1].grid(True, linestyle='--', alpha=0.7)

    plt.savefig("data/full_results_plot.png", dpi=150, bbox_inches='tight')
    print("Plots generated successfully!")

if __name__ == "__main__":
    plot()