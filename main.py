import numpy as np
from src.circuit import FlatCircuit
from src.r1cs import R1CS
from src.witness import WitnessGenerator

def id_card_circuit():
    # --- STEP 1: DEFINE CIRCUIT ---
    circuit = FlatCircuit()
    
    current_year = "2026"
    dob = "1990"    # Secret input
    threshold = "21"
    
    # Age = 2026 - 1990
    age = circuit.sub(current_year, dob, output_name="age")
    # Result = Age - 21
    result = circuit.sub(age, threshold, output_name="result")
    
    # --- STEP 2: COMPILE TO R1CS ---
    print("\n--- 1. R1CS Compilation ---")
    r1cs = R1CS(circuit)
    
    # --- STEP 3: EXECUTE (GENERATE WITNESS) ---
    print("\n--- 2. Witness Generation ---")
    # This is where we provide the SECRET data
    input_data = {
        "2026": 2026,
        "1990": 1990,
        "21": 21
    }
    
    wg = WitnessGenerator(circuit, r1cs)
    w = wg.generate(input_data)
    
    print(f"\nWitness Vector w: {w}")
    print(f"Variables map: {r1cs.var_map}")

    # --- STEP 4: VERIFY (THE PROOF) ---
    print("\n--- 3. Verification (A*B - C = 0) ---")
    # For a ZK-SNARK to be valid, (A . w) * (B . w) - (C . w) must equal 0
    # for EVERY constraint.
    
    verified = True
    for i in range(len(r1cs.A)):
        # Dot product of vectors
        a_val = np.dot(r1cs.A[i], w)
        b_val = np.dot(r1cs.B[i], w)
        c_val = np.dot(r1cs.C[i], w)
        
        # Check: A * B = C
        check = (a_val * b_val) - c_val
        
        if check == 0:
            print(f"Constraint {i} passed: {a_val} * {b_val} = {c_val}")
        else:
            print(f"Constraint {i} FAILED: {a_val} * {b_val} != {c_val}")
            verified = False
            
    if verified:
        print("\nSUCCESS: The Proof is Valid! You are over 21.")
    else:
        print("\nFAILURE: Math does not check out.")

if __name__ == "__main__":
    id_card_circuit()