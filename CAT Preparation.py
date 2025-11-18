import stim
from qiskit import QuantumCircuit
from mqt.qecc.circuit_synthesis import CatStatePreparationExperiment, cat_state_balanced_tree



'''
circ = stim.Circuit()
p = 0.05  # physical error rate

def noisy_cnot(circ: stim.Circuit, ctrl: int, trgt: int, p: float) -> None:
    circ.append_operation("CX", [ctrl, trgt])
    circ.append_operation("DEPOLARIZE2", [ctrl, trgt], p)

circ.append_operation("H", [0])
circ.append_operation("DEPOLARIZE1", range(8), p)

noisy_cnot(circ, 0, 4, p)

noisy_cnot(circ, 0, 2, p)
noisy_cnot(circ, 4, 6, p)

noisy_cnot(circ, 0, 1, p)
noisy_cnot(circ, 2, 3, p)
noisy_cnot(circ, 4, 5, p)
noisy_cnot(circ, 6, 7, p)

QuantumCircuit.from_qasm_str(circ.without_noise().to_qasm(open_qasm_version=2)).draw('mpl').savefig('circuit.png')
'''

if __name__ == '__main__':
    p = 0.05  # physical error rate

    w = 8
    data = cat_state_balanced_tree(w)
    ancilla = cat_state_balanced_tree(w)

    # Create different permutations
    pi_1 = list(range(w))

    pi_2 = list(range(w))
    pi_2[0] = 15
    pi_2[15] = 0

    pi_3 = [0, 1, 6, 10, 13, 3, 5, 15, 2, 8, 11, 14, 4, 9, 12, 7]

    # Create experiments with different permutations
    e_1 = CatStatePreparationExperiment(data, ancilla, pi_1)
    e_2 = CatStatePreparationExperiment(data, ancilla, pi_2)
    e_3 = CatStatePreparationExperiment(data, ancilla, pi_3)

    # Draw and save circuits
    QuantumCircuit.from_qasm_str(e_1.circ.without_noise().to_qasm(open_qasm_version=2)).draw('mpl').savefig('cat_8_pi1_identity.png')
    QuantumCircuit.from_qasm_str(e_2.circ.without_noise().to_qasm(open_qasm_version=2)).draw('mpl').savefig('cat_8_pi2_swap.png')
    QuantumCircuit.from_qasm_str(e_3.circ.without_noise().to_qasm(open_qasm_version=2)).draw('mpl').savefig('cat_8_pi3_optimized.png')

    e_1.plot_one_p(p, n_samples=100000)
    e_2.plot_one_p(p, n_samples=100000)
    e_3.plot_one_p(p, n_samples=100000)

    print(f"\nCreated {w}-qubit CAT state preparation experiments with 3 different permutations")
    print(f"pi_1 (identity): {pi_1}")
    print(f"pi_2 (swap 0,15): {pi_2}")
    print(f"pi_3 (optimized): {pi_3}")
    print("\nCircuits saved:")
    print("  - cat_16_pi1_identity.png")
    print("  - cat_16_pi2_swap.png")
    print("  - cat_16_pi3_optimized.png")
