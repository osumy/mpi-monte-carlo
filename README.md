# Distributed Monte Carlo Integration using MPI

This repository contains a high-performance distributed computing project that approximates the solution of a first-order Ordinary Differential Equation (ODE) using the **Monte Carlo Integration** method. The system is designed under the **Master-Worker paradigm** leveraging the Message Passing Interface (MPI) via `mpi4py`.

## 📌 Project Overview
The core objective is to evaluate the function $u(x)$ defined by:
$$u'(x) = \sin(x), \quad u(0) = 0$$

Which translates into the definite integral:
$$u(x) = \int_{0}^{x} \sin(t) \, dt$$

Using stochastic uniform sampling, the continuous integral is transformed into a distributed average estimation problem, making it highly parallelizable across multiple processing units.

---

## 📂 Project Structure
``` text
├── config.json          # Centralized configuration parameters
├── runner.py            # Automated experiment orchestrator
├── requirements.txt     # Python dependencies
├── README.md            # Repository documentation
└── src/
    ├── monte_carlo.py   # Vectorized Monte Carlo mathematical engine
    ├── main.py          # Parallel MPI runtime execution
    └── analyzer.py      # Statistical parsing and plot generator
```

## 🛠️ Prerequisites & Installation

### 1. MPI System Driver (Windows)
Since this project runs on Windows distributed emulation, you must install the official **Microsoft MPI (MS-MPI)** runtime:
* Download and install msmpisetup.exe and msmpisdk.msi from the Official Microsoft MPI Downloads.

### 2. Python Environment Setup
Clone the repository and install the required numerical and visualization stack using pip:
```bash
git clone https://github.com/osumy/cp-1.git
cd cp-1
pip install -r requirements.txt
```

## ⚙️ Configuration (config.json)
You can tweak the parameters dynamically without rewriting the source code:
```json
{
    "x_value": 2.0,
    "total_samples_performance": 50000000,
    "accuracy_samples": [10, 100, 1000, 10000, 100000, 1000000, 10000000],
    "performance_processes": [1, 2, 4, 8]
}
```
## 🚀 How To Run
Instead of manually executing individual command-line arguments, a unified automated Orchestrator is provided. Run the following command in the root directory:

```bash
python runner.py
```

### What happens under the hood?
1. Accuracy Mode: Executes "mpiexec -n 4 python src/main.py accuracy" to record logarithmic error drops from N=10^1 to N=10^7.
2. Performance Mode: Loops through process pools [1, 2, 4, 8] via "mpiexec -n <P> python src/main.py performance" utilizing 50,000,000 global samples.
3. Data Analysis: Invokes src/analyzer.py to parse CSV outputs, compute Speedup/Efficiency curves, and save analytical graphs in a /plots directory.



## 📊 Empirical Analysis Summary

### Hardware Environment
* **Processor:** 13th Gen Intel(R) Core(TM) i7-13620H (10 Physical Cores: 6 P-cores / 4 E-cores | 16 Threads)
* **OS Environment:** Windows Subsystem with MS-MPI bindings

### Key Findings
* **Mathematical Convergence:** The error strictly drops following the theoretical O(1/sqrt(N)) law of stochastic convergence, reaching a high-precision absolute error of 3.95 x 10^-5 at 10^7 samples.
* **Parallel Bottlenecks:** Parallel scalability achieves near-perfect efficiency (97.3%) at P=2 and 89.3% at P=4. However, performance drops to 69.9% at P=8. This behavior perfectly models Amdahl's Law due to communication overhead and hybrid core heterogeneity (scheduling tasks onto Intel's single-threaded E-cores or sharing hyper-threaded FPUs on P-cores).

---

## 🧑‍💻 Author
* **Developer:** AmirAli Araghi
* **Course:** Concurrent Programming (Spring 2025)
* **Instructor:** Dr. Mehdi Movahedian Moqadam

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
