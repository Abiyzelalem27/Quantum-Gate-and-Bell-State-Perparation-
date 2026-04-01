

<<<<<<< HEAD
# Bell_state

## Features
- **Single-Qubit Gates:** X, Y, Z, Hadamard (H), S, T, and general rotation gates.  
- **Two-Qubit Gates:** Controlled operations like CNOT for creating entanglement.  
- **Bell States:** Prepare all four maximally entangled Bell states (Φ⁺, Φ⁻, Ψ⁺, Ψ⁻).  
- **Visualizations:** Bloch sphere visualizations for single-qubit states.  
- **Educational:** Step-by-step demonstrations of qubit transformation  
<<<<<<< HEAD
Your local changes
=======
Incoming changes from rebase
>>>>>>> commit-hash
=======
# Bell State 

Quantum gates are the fundamental building blocks of quantum circuits. They manipulate the state of qubits, enabling quantum computations and algorithms. Quantum gates are **unitary operations**, meaning they preserve total probability and keep the system in a valid quantum state.

---

## ✅ Quantum Gates

### 🔹 Single-Qubit Gates
Single-qubit gates operate on **one qubit** at a time. They change the qubit state through operations such as **rotations, bit-flips, and phase shifts**.

Examples include:
- Pauli gates: **X, Y, Z**
- Hadamard: **H**
- Phase gates: **S, T**
- General rotation gates: **Rx, Ry, Rz**

---

### 🔹 Multi-Qubit Gates
Multi-qubit gates act on **two or more qubits simultaneously**, enabling:
- **Entanglement**
- **Conditional operations**
- Multi-qubit quantum algorithms

Examples include:
- **CNOT**
- **CZ**
- **Toffoli (CCX)**

---

## ✅ Bell State Preparations

Bell states are **maximally entangled two-qubit states**.  
They **cannot be created using only single-qubit gates** — an **entangling gate** such as **CNOT** is required.

All four Bell states can be generated from the initial ground state:

\[
|00\rangle
\]

---

### ✅ 1) Φ⁺ (Phi Plus)

\[
|\Phi^{+}\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
\]

**Preparation**
1. Start with \(|00\rangle\)
2. Apply **Hadamard (H)** on qubit 0
3. Apply **CNOT** (control = qubit 0, target = qubit 1)

✅ Circuit:

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

print(qc.draw(output="text"))
>>>>>>> A
