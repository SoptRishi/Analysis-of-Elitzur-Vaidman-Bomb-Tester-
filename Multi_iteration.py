# iterative_zeno.py
"""
Iterative Quantum Zeno simulation for high-efficiency IFM.
Varies cycle count (N) to demonstrate the suppression of the explosion rate.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

CYCLES_TO_TEST = [2, 3, 4, 5, 10, 50]
SHOTS = 10000

def run_zeno_series():
    results = {'N': [], 'Success': [], 'Exploded': [], 'Inconclusive': []}
    backend = AerSimulator()

    print(f"Running Zeno sweep for N={CYCLES_TO_TEST}...")

    for n in CYCLES_TO_TEST:
        qc = QuantumCircuit(2, n + 1)
        
        # Rotation angle theta = pi/N to ensure full transfer to |1> over N cycles
        theta = np.pi / n
        
        for step in range(n):
            qc.ry(theta, 0)      
            qc.cx(0, 1)          # Bomb interaction
            qc.measure(1, step)  # Zeno measurement
            qc.reset(1)          # Collapse/Reset
        
        qc.measure(0, n)
        
        # Execute
        counts = backend.run(qc, shots=SHOTS).result().get_counts()
        
        # Data processing
        exp_count = 0
        succ_count = 0
        inc_count = 0
        
        for bitstr, count in counts.items():
            # bitstr format: "q_photon q_checkN ... q_check1"
            bomb_checks = bitstr[1:]
            photon_state = bitstr[0]
            
            if '1' in bomb_checks:
                exp_count += count
            elif photon_state == '0':
                succ_count += count
            else:
                inc_count += count

        # Append stats
        results['N'].append(n)
        results['Success'].append(succ_count / SHOTS)
        results['Exploded'].append(exp_count / SHOTS)
        results['Inconclusive'].append(inc_count / SHOTS)
        
        print(f"N={n:2d} | Success: {succ_count/SHOTS:.2%} | Exploded: {exp_count/SHOTS:.2%}")

    plot_zeno_histogram(results)

def plot_zeno_histogram(data):
    x_idx = np.arange(len(data['N']))
    width = 0.25
    
    plt.figure(figsize=(10, 6))
    
    # Plotting grouped bars
    plt.bar(x_idx - width, data['Success'], width, label='Success', color='limegreen', edgecolor='k')
    plt.bar(x_idx, data['Exploded'], width, label='Exploded', color='salmon', edgecolor='k')
    plt.bar(x_idx + width, data['Inconclusive'], width, label='Inconclusive', color='lightgray', edgecolor='k')
    
    plt.xlabel('Cycles (N)')
    plt.ylabel('Probability')
    plt.title('Efficiency Scaling with Zeno Cycles')
    plt.xticks(x_idx, [f"N={n}" for n in data['N']])
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_zeno_series()
