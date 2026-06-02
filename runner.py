import subprocess
import json
import os

def run_command(command):
    print(f"Executing: {command}")
    subprocess.run(command, shell=True, check=True)

def main():
    if not os.path.exists('config.json'):
        print("Error: config.json not found!")
        return

    with open('config.json', 'r') as f:
        config = json.load(f)
    
    procs = config.get('performance_processes', [1, 2, 4, 8])

    print("=== STARTING AUTOMATED EXPERIMENTS ===")

    if os.path.exists('data/accuracy.csv'):
        os.remove('data/accuracy.csv')
    if os.path.exists('data/performance.csv'):
        os.remove('data/performance.csv')

    print("\n--- Running Accuracy Mode ---")
    run_command("mpiexec -n 4 python src/main.py accuracy")

    print("\n--- Running Performance Mode ---")
    for p in procs:
        run_command(f"mpiexec -n {p} python src/main.py performance")

    print("\n--- Generating Plots ---")
    run_command("python src/analyzer.py")

    print("\n=== EXPERIMENTS COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()