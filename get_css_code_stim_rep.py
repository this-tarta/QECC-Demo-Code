import stim
import qiskit
from mqt.qecc import CSSCode
from mqt.qecc.circuit_synthesis.state_prep import heuristic_prep_circuit, gate_optimal_verification_circuit
from mqt.qecc.circuit_synthesis import qiskit_to_stim_circuit

if __name__ == '__main__':
    steane_code = CSSCode.from_code_name("Steane")
    non_ft_sp = heuristic_prep_circuit(steane_code, zero_state=True)

    print("Non-FT Steane preparation circuit:")
    print(non_ft_sp.circ.draw(output="text", initial_state=True))
    non_ft_stim_str = str(non_ft_sp.circ.to_stim_circuit())
    print(non_ft_stim_str)

    ft_sp = gate_optimal_verification_circuit(non_ft_sp)
    print("FT Steane preparation circuit:")
    print(ft_sp.draw(output="text", initial_state=True))
    ft_stim_str = str(qiskit_to_stim_circuit(ft_sp))
    print(ft_stim_str)