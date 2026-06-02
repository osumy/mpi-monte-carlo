import os
import pandas as pd
import matplotlib.pyplot as plt

def make_plots():
    if not os.path.exists('plots'):
        os.makedirs('plots')

    if os.path.exists('data/accuracy.csv'):
        df_acc = pd.read_csv('data/accuracy.csv')
        df_acc = df_acc.drop_duplicates(subset=['N']).sort_values('N')
        
        plt.figure(figsize=(8, 5))
        plt.plot(df_acc['N'], df_acc['Error'], marker='o', color='red', linewidth=2)
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Monte Carlo Integration: Error Convergence', fontsize=12)
        plt.xlabel('Number of Samples (N)')
        plt.ylabel('Absolute Error')
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig('plots/error_convergence.png', dpi=300)
        plt.close()
        print("Saved plot: plots/error_convergence.png")

    if os.path.exists('data/performance.csv'):
        df_perf = pd.read_csv('data/performance.csv')
        df_perf = df_perf.drop_duplicates(subset=['Processes']).sort_values('Processes')
        
        t1_data = df_perf[df_perf['Processes'] == 1]
        if not t1_data.empty:
            t1 = t1_data['Time'].values[0]
            df_perf['Speedup'] = t1 / df_perf['Time']
            df_perf['Efficiency'] = df_perf['Speedup'] / df_perf['Processes']
            
            plt.figure(figsize=(8, 5))
            plt.plot(df_perf['Processes'], df_perf['Speedup'], marker='s', color='blue', label='Actual Speedup')
            plt.plot(df_perf['Processes'], df_perf['Processes'], linestyle='--', color='gray', label='Ideal')
            plt.title('Parallel Speedup', fontsize=12)
            plt.xlabel('Number of Processes')
            plt.ylabel('Speedup (S)')
            plt.legend()
            plt.grid(True, alpha=0.5)
            plt.tight_layout()
            plt.savefig('plots/speedup.png', dpi=300)
            plt.close()
            print("Saved plot: plots/speedup.png")
            
            plt.figure(figsize=(8, 5))
            plt.plot(df_perf['Processes'], df_perf['Efficiency'] * 100, marker='^', color='green')
            plt.axhline(100, linestyle='--', color='gray')
            plt.title('Parallel Efficiency', fontsize=12)
            plt.xlabel('Number of Processes')
            plt.ylabel('Efficiency (%)')
            plt.ylim(0, 110)
            plt.grid(True, alpha=0.5)
            plt.tight_layout()
            plt.savefig('plots/efficiency.png', dpi=300)
            plt.close()
            print("Saved plot: plots/efficiency.png")
        else:
            print("Error: Running with 1 process is required to compute speedup.")

if __name__ == "__main__":
    make_plots()