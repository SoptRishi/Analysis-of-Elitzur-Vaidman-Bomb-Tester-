
"""
script to visualize Qiskit circuits for the EV protocol.
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def get_basic_circuit():
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)
    
    qc.h(0)
    qc.barrier()
    qc.cx(0, 1)
    qc.barrier()
    qc.h(0)
    qc.barrier()
    qc.measure(qr, cr)
    
    return qc

def get_iterative_circuit(n=3):
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(n + 1, 'c')
    qc = QuantumCircuit(qr, cr)
    
    theta = np.pi / n
    
    for i in range(n):
        qc.barrier()
        qc.ry(theta, 0)
        qc.cx(0, 1)
        qc.measure(1, i)
        qc.reset(1)
        
    qc.barrier()
    qc.measure(0, n)
    return qc

if __name__ == "__main__":
    print("--- Basic Setup (N=1) ---")
    print(get_basic_circuit().draw(output='text'))
    
    print("\n--- Iterative Setup (N=4) ---")
    print(get_iterative_circuit(4).draw(output='text'))
  
