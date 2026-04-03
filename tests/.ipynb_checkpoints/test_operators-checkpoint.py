


import numpy as np
from bell_state import (
    I, X, Y, Z, H, S, T, P0, P1,
    controlled_gate, projectors, U_N_qubits, U_one_gate, U_two_gates,
    ket0, ket1, ket_plus, ket_minus, dm
)


def test_single_qubit_gates():
    """Test all single-qubit gates for self-inverse and unitarity."""
    assert np.allclose(I @ I, I)
    assert np.allclose(X @ X, I)
    assert np.allclose(Y @ Y, I)
    assert np.allclose(Z @ Z, I)
    assert np.allclose(H @ H, I)
    assert np.allclose(S @ S, Z)
    assert np.allclose(T @ T @ T @ T, Z)

def test_kets_and_dm():
    """Test standard kets for normalization and density matrices for Hermiticity."""
    for ket in [ket0(), ket1(), ket_plus(), ket_minus()]:
        assert np.isclose(np.linalg.norm(ket), 1)
        rho = dm(ket)
        assert np.allclose(rho, rho.conj().T)
        assert np.isclose(np.trace(rho), 1)


def test_controlled_gate():
    """Test controlled gates: CNOT, CZ, and error handling."""
    N = 2
    # CNOT control=0, target=1
    C_X = controlled_gate(X, 0, 1, N)
    state = np.kron(ket1(), ket0())
    out = C_X @ state
    expected = np.kron(ket1(), ket1())
    assert np.allclose(out, expected)
    
    # CZ gate
    C_Z = controlled_gate(Z, 0, 1, N)
    state = np.kron(ket1(), ket1())
    out = C_Z @ state
    expected = np.kron(ket1(), -ket1())
    assert np.allclose(out, expected)
    
    # Error when control == target
    try:
        controlled_gate(X, 0, 0, N)
        assert False  # should not reach here
    except ValueError:
        pass


def test_U_one_two_gates():
    """Test single-qubit and two-qubit gate embeddings."""
    # Single qubit
    state = U_one_gate(X, 0, 2) @ np.kron(ket0(), ket0())
    expected = np.kron(ket1(), ket0())
    assert np.allclose(state, expected)

    # Two qubits i != j
    state2 = U_two_gates(X, H, 0, 1, 2) @ np.kron(ket0(), ket0())
    expected2 = np.kron(ket1(), ket_plus())
    assert np.allclose(state2, expected2)

    # Two qubits i == j
    state3 = U_two_gates(H, X, 1, 1, 2) @ np.kron(ket0(), ket0())
    expected3 = np.kron(ket0(), H @ X @ ket0())
    assert np.allclose(state3, expected3)


def test_projectors():
    """Test projectors for Hermiticity, idempotency, orthogonality, and sum to identity."""
    P = projectors(2)
    for Pi in P:
        assert np.allclose(Pi.conj().T, Pi)
        assert np.allclose(Pi @ Pi, Pi)
    assert np.allclose(P[0] @ P[1], 0)
    assert np.allclose(P[1] @ P[0], 0)
    I2 = np.eye(2)
    assert np.allclose(sum(P), I2)
