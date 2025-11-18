import stim
import qiskit
from mqt.qecc import CSSCode
from mqt.qecc.circuit_synthesis import VerificationNDFTStatePrepSimulator, CircuitLevelNoiseIdlingParallel

if __name__ == '__main__':
    steane_code = CSSCode.from_code_name("Steane")
    baseline_str ="""
        H 0 1
        CX 0 2 1 0
        H 3
        CX 3 5 3 4 0 4 5 6 1 5 2 6 2 7 4 7 5 7
        MR 7
    """
    # circ_str ="""
    #     R 2 4 5 6
    #     RX 0 1 3
    #     CX 3 5 0 2 5 6 3 4 1 0 2 6 1 5 0 4
    #     R 9 11 12 13
    #     RX 7 8 10
    #     CX 10 12 7 9 12 13 10 11 8 7 9 13 8 12 7 11
    #     CX 0 7 1 8 2 9 3 10 4 11 5 12 6 13
    #     M 7 8 9 10 11 12 13
    # """
    circ_str = """
        R 2 4 5 6
        RX 0 1 3
        CX 3 5 0 2 5 6 3 4 1 0 2 6 1 5 0 4
        CX 0 7 1 8 2 9 3 10 4 11 5 12 6 13
        M 7 8 9 10 11 12 13
    """
    baseline_circ = stim.Circuit(baseline_str)
    circ = stim.Circuit(circ_str)
    baseline_q_circ = qiskit.QuantumCircuit.from_qasm_str(baseline_circ.to_qasm(open_qasm_version=2))
    q_circ = qiskit.QuantumCircuit.from_qasm_str(circ.to_qasm(open_qasm_version=2))

    ps = [0.1, 0.05, 0.04, 0.03, 0.02, 0.01, 0.009, 0.008]
    baseline_simulator = VerificationNDFTStatePrepSimulator(baseline_q_circ, steane_code, zero_state=True)
    baseline_simulator.plot_state_prep(
        ps, min_errors=50, p_idle_factor=0.01
    )
    simulator = VerificationNDFTStatePrepSimulator(q_circ, steane_code, zero_state=True)
    simulator.plot_state_prep(
        ps, min_errors=50, p_idle_factor=0.01
    )

    p = 0.05
    noise = CircuitLevelNoiseIdlingParallel(p_tqg=p, p_sqg=p, p_init=p, p_meas=p, p_idle=p/100)

    baseline_error_rate, baseline_acceptance_rate, _, _ = baseline_simulator.logical_error_rate(noise, shots=100000)
    error_rate, acceptance_rate, _, _ = simulator.logical_error_rate(noise, shots=100000)
    print(f'Baseline output: physical error rate {p}, logical error rate {float(baseline_error_rate)}, acceptance rate {baseline_acceptance_rate}')
    print(f'LLM output: physical error rate {p}, logical error rate {float(error_rate)}, acceptance rate {acceptance_rate}')
    