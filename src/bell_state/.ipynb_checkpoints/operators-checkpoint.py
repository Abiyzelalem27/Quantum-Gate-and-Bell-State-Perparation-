import numpy as np

import numpy as np
from collections import Counter
import itertools 
from scipy import sparse 
import scipy
import matplotlib.pyplot as plt 
import math
import random  

I = np.array([[1, 0],
              [0, 1]], dtype=complex)
X = np.array([[0, 1],
              [1, 0]], dtype=complex)
Y = np.array([[0, -1j],
              [1j,  0]], dtype=complex)
Z = np.array([[1,  0],
              [0, -1]], dtype=complex)
H = 1 / np.sqrt(2) * np.array([[1,  1],
                               [1, -1]], dtype=complex)
P0 = np.array([[1, 0],
               [0, 0]], dtype=complex)
P1 = np.array([[0, 0],
               [0, 1]], dtype=complex)
S = np.array([[1, 0],
              [0, 1j]], dtype=complex)
T = np.array([[1, 0],
              [0, np.e**(1j * np.pi / 4)]], dtype=complex)


def controlled_gate(U, control, target, N):
    """
    Controlled-U gate on an N-qubit register.
    Implements the projector decomposition:
        C_U = P0(control) ⊗ I  +  P1(control) ⊗ U(target)
    """
    if control == target:
        raise ValueError("Control and target must be different")
    # Operator acting on the subspace where the control qubit is |0⟩
    P0_ops = [
        P0 if i == control else I
        for i in range(N)
    ]

    # Operator acting on the subspace where control qubit is |1⟩
    P1_ops = [
        P1 if i == control else U if i == target else I
        for i in range(N)
    ]

    return U_N_qubits(P0_ops) + U_N_qubits(P1_ops)

 

def projectors(dim):
    """
    Generate computational basis projectors {|i><i|} with the given dimension.
    """
    projectors = []
    for i in range(dim):
        ket = np.zeros(dim, dtype=complex)
        ket[i] = 1
        P = np.outer(ket, ket)
        projectors.append(P)
    return projectors
    
def U_N_qubits(ops):
    """
    Constructs an N-qubit operator using tensor products.

    Parameters
    ops : single-qubit operators.
    """
    U = ops[0]
    for op in ops[1:]:
        U = np.kron(U, op)
    return U


def U_one_gate(V, i, N):
    """
    Applies a single-qubit gate to qubit i
    in an N-qubit system.

    Parameters
    V : Single-qubit gate.
    i : Target qubit index.
    N : Total number of qubits.
    """
    ops = [I] * N
    ops[i] = V
    return U_N_qubits(ops)


def U_two_gates(V, W, i, j, N):
    """
    Applies two single-qubit gates to an N-qubit system.
    If i != j:
        applies V on qubit i and W on qubit j.
    If i == j:
        applies the composed gate V @ W on qubit i,
        preserving operator ordering.
    """
    ops = [I] * N
    if i == j:
        ops[i] = V @ W
    else:
        ops[i] = V
        ops[j] = W
    return U_N_qubits(ops)

def ket0():
    return np.array([1, 0], dtype=complex)

def ket1():
    return np.array([0, 1], dtype=complex)

def ket_plus():
    return (ket0() + ket1()) / np.sqrt(2)

def ket_minus():
    return (ket0() - ket1()) / np.sqrt(2)

def dm(psi):
    """
    Construct a density matrix from a pure state |psi⟩.

    ρ = |psi⟩⟨psi|
    """
    psi = psi/np.linalg.norm(psi)
    return np.outer(psi, psi.conj())

def rotation_gate(theta, n):
    """
    This function implements a unitary rotation of a single qubit
    by an angle `theta` around an axis `n` on the Bloch sphere.

    The rotation generator is constructed as N = n · σ,
    where σ = (X, Y, Z) are the Pauli matrices.

    Parameters
    theta : Rotation angle
    n : Rotation axis
    """
    nx, ny, nz = n
    N = nx * X + ny * Y + nz * Z
    R = np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * N 
    return R

def toffoli_gate(U):
    """
    General 2-control, 1-target Toffoli gate (CCU).
    U: 2x2 unitary matrix to apply to target qubit if both controls are |1>.
    Returns: 8x8 unitary matrix representing the 3-qubit gate.
    """
    # Construct 8x8 Toffoli as sum of tensor products
    # Cases where first or second control is 0 → do nothing
    term0 = np.kron(P0, I)      # control1 = 0
    term0 = np.kron(term0, I)   # tensor with control2 and target
    term1 = np.kron(P1, P0)     # control1=1, control2=0
    term1 = np.kron(term1, I)   # target unchanged
    # Case where both controls = 1 → apply U to target
    term2 = np.kron(P1, P1)
    term2 = np.kron(term2, U)
    # Full Toffoli matrix
    T = term0 + term1 + term2
    return T 


