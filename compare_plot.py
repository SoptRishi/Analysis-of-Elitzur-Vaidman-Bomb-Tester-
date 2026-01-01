# plot_results.py
"""
Plots the theoretical efficiency limit of the EV protocol: P = cos(pi/2N)^(2N).
"""

import numpy as np
import matplotlib.pyplot as plt

def main():
    cycles = np.array([1, 2, 5, 10, 20, 50, 100])
    
    # Calculate theoretical max efficiency
    # Angle theta = pi / (2N) for the physical system equivalent
    theta_phys = np.pi / (2 * cycles)
    p_success = np.cos(theta_phys)**(2 * cycles)

    plt.figure(figsize=(9, 6))
    
    plt.plot(cycles, p_success, 'o-', color='navy', linewidth=2, label='Theory Limit')
    plt.axhline(1.0, color='red', linestyle='--', alpha=0.7, label='Ideal (100%)')
    
    plt.title("Elitzur-Vaidman Efficiency Limit")
    plt.xlabel("Number of Cycles (N)")
    plt.ylabel("Success Probability")
    plt.ylim(0, 1.05)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    # Annotate key data points
    for x, y in zip(cycles, p_success):
        if x in [1, 5, 20, 100]:
            plt.annotate(f'{y:.1%}', xy=(x, y), xytext=(0, 8), 
                         textcoords='offset points', ha='center', fontsize=9, weight='bold')

    plt.tight_layout()
    plt.savefig('efficiency_curve.png')
    plt.show()

if __name__ == "__main__":
    main()
