from mqt.qecc import CSSCode
from mqt.qecc.circuit_synthesis import gate_optimal_prep_circuit, heuristic_prep_circuit
from mqt.qecc.circuit_synthesis import gate_optimal_verification_circuit
from mqt.qecc.circuit_synthesis import VerificationNDFTStatePrepSimulator, CircuitLevelNoiseIdlingParallel

from mqt.qecc.circuit_synthesis import heuristic_prep_circuit
from mqt.qecc.codes import SquareOctagonColorCode
from mqt.qecc.circuit_synthesis import naive_verification_circuit
from mqt.qecc.circuit_synthesis import DeterministicVerificationHelper
import time

if __name__ == '__main__':
    steane_code = CSSCode.from_code_name("Steane")
    print(steane_code.stabs_as_pauli_strings())

    print("\n" + "="*60)
    print("Generating non-FT preparation circuit...")
    start_time = time.time()
    non_ft_sp = heuristic_prep_circuit(steane_code, zero_state=True) # gate_optimal_prep_circuit(steane_code, zero_state=True) 
    elapsed = time.time() - start_time
    print(f"✓ Non-FT circuit generated in {elapsed:.2f} seconds")

    non_ft_sp.circ.draw(output="mpl", initial_state=True).savefig("steane_non_ft_prep.png")
    print("Circuit saved to steane_non_ft_prep.png")

    print("\n" + "="*60)
    print("Generating FT verification circuit...")
    start_time = time.time()
    ft_sp = gate_optimal_verification_circuit(non_ft_sp)
    elapsed = time.time() - start_time
    print(f"✓ FT circuit generated in {elapsed:.2f} seconds")

    ft_sp.draw(output="mpl", initial_state=True).savefig("steane_ft_prep.png")
    print("Circuit saved to steane_ft_prep.png")

    p = 0.05
    noise = CircuitLevelNoiseIdlingParallel(p_tqg=p, p_sqg=p, p_init=p, p_meas=p, p_idle=p/100)

    non_ft_simulator = VerificationNDFTStatePrepSimulator(
        non_ft_sp.circ, code=steane_code, zero_state=True
    )
    ft_simulator = VerificationNDFTStatePrepSimulator(
        ft_sp, code=steane_code, zero_state=True
    )

    print("\n" + "="*60)
    print("Generating Color Code (5,5,5) circuits...")
    cc = SquareOctagonColorCode(5)
    
    print("\nGenerating heuristic non-FT preparation circuit...")
    start_time = time.time()
    cc_non_ft_sp = heuristic_prep_circuit(cc, zero_state=True, optimize_depth=True)
    elapsed = time.time() - start_time
    print(f"✓ Color code non-FT circuit generated in {elapsed:.2f} seconds")

    cc_non_ft_sp.circ.draw(output="mpl", initial_state=True, scale=0.7).savefig("cc5_non_ft_prep.png")
    print("Circuit saved to cc5_non_ft_prep.png")

    print("\nGenerating gate-optimal FT verification circuit...")
    start_time = time.time()
    cc_ft_sp = gate_optimal_verification_circuit(
        cc_non_ft_sp, max_timeout=4, max_ancillas=3
    )
    elapsed = time.time() - start_time
    print(f"✓ Color code FT circuit generated in {elapsed:.2f} seconds")

    cc_ft_sp.draw(output="mpl", initial_state=True, fold=-1, scale=0.2).savefig("cc5_ft_prep.png")
    print("Circuit saved to cc5_ft_prep.png")

    print("\nGenerating naive verification circuit...")
    start_time = time.time()
    cc_ft_naive = naive_verification_circuit(cc_non_ft_sp)
    elapsed = time.time() - start_time
    print(f"✓ Naive FT circuit generated in {elapsed:.2f} seconds")

    print(
        f"\nCNOTs required for naive FT state preparation: {cc_ft_naive.num_nonlocal_gates()}"
    )
    print(
        f"CNOTs required for optimized FT state preparation: {cc_ft_sp.num_nonlocal_gates()}"
    )

    cc_simulator = VerificationNDFTStatePrepSimulator(cc_ft_sp, code=cc, zero_state=True)

    ps = [0.1, 0.05, 0.04, 0.03, 0.02, 0.01, 0.009, 0.008]

    ft_simulator.plot_state_prep(
        ps, min_errors=50, p_idle_factor=0.01
    )  # simulate Steane code as comparison
    cc_simulator.plot_state_prep(ps, min_errors=50, p_idle_factor=0.01)

    det_helper = DeterministicVerificationHelper(non_ft_sp)
    det_verify = det_helper.get_solution(use_optimal_verification=True)
    det_verify_x, det_verify_z = det_verify
    print(f'det_verify_x.stabs: {det_verify_x.stabs}')
    print(f'det_verify_x.det_correction: {det_verify_x.det_correction}')
    print(f'det_verify_x.hook_corrections: {det_verify_x.hook_corrections}')
