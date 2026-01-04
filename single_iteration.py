
"""
Simulates the single-shot Elitzur-Vaidman interferometer (N=1).
Generates statistics for Explosion vs. Interaction-Free Measurement (IFM).
"""

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

SHOTS = 10000

def run_experiment():
    # Standard Mach-Zehnder with a bomb in the lower arm
    qc = QuantumCircuit(2, 2)
    qc.h(0)       
    qc.cx(0, 1)   
    qc.h(0)       
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()
    job = backend.run(qc, shots=SHOTS)
    counts = job.result().get_counts()

    # Parse results: q1=1 is explosion, q0 determining path
    exploded = counts.get('10', 0) + counts.get('11', 0)
    success = counts.get('01', 0)
    inconclusive = counts.get('00', 0)
    
    total = sum(counts.values())
    probs = {
        'Exploded': exploded / total,
        'Success (IFM)': success / total,
        'Inconclusive': inconclusive / total
    }

    print(f"--- Results (N=1, Shots={total}) ---")
    for k, v in probs.items():
        print(f"{k:<15}: {v:.2%}")

    plot_results(probs)

def plot_results(probs):
    labels = list(probs.keys())
    values = list(probs.values())
    colors = ['salmon', 'limegreen', 'lightgray'] # Exploded, Success, Inc
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=colors, edgecolor='k', alpha=0.9)
    
    plt.title('Single-Shot EV Experiment Results')
    plt.ylabel('Probability')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f"{yval:.1%}", ha='center', weight='bold')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_experiment()
