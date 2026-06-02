import sys
import os
import json
from mpi4py import MPI
from monte_carlo import MonteCarloIntegrator

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    with open('config.json', 'r') as f:
        config = json.load(f)

    x_val = config['x_value']
    integrator = MonteCarloIntegrator(x_val)

    mode = sys.argv[1] if len(sys.argv) > 1 else "accuracy"

    if rank == 0 and not os.path.exists('data'):
        os.makedirs('data')

    if mode == "accuracy":
        samples_to_test = config['accuracy_samples']
        
        for n in samples_to_test:
            local_n = n // size
            
            comm.Barrier()
            start_t = MPI.Wtime()
            
            my_sum = integrator.calculate_local_sum(local_n)
            total_sum = comm.reduce(my_sum, op=MPI.SUM, root=0)
            
            comm.Barrier()
            end_t = MPI.Wtime()
            
            if rank == 0:
                ans = (x_val / n) * total_sum
                exact = integrator.get_exact_value()
                err = abs(exact - ans)
                
                file_path = 'data/accuracy.csv'
                write_header = not os.path.exists(file_path)
                with open(file_path, 'a', newline='') as f:
                    if write_header:
                        f.write("N,Approx,Exact,Error\n")
                    f.write(f"{n},{ans},{exact},{err}\n")
                print(f"N: {n} | Error: {err:.6e}")

    elif mode == "performance":
        total_samples = config['total_samples_performance']
        local_n = total_samples // size
        
        comm.Barrier()
        start_t = MPI.Wtime()
        
        my_sum = integrator.calculate_local_sum(local_n)
        total_sum = comm.reduce(my_sum, op=MPI.SUM, root=0)
        
        comm.Barrier()
        end_t = MPI.Wtime()
        
        if rank == 0:
            elapsed = end_t - start_t
            file_path = 'data/performance.csv'
            write_header = not os.path.exists(file_path)
            with open(file_path, 'a', newline='') as f:
                if write_header:
                    f.write("Processes,Total_N,Time\n")
                f.write(f"{size},{total_samples},{elapsed}\n")
            print(f"Procs: {size} | Time: {elapsed:.4f}s")

if __name__ == "__main__":
    main()