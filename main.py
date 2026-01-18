import sys
import time
from src.circuit import FlatCircuit
from src.r1cs import R1CS
from src.witness import WitnessGenerator

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

def get_user_input():
    print("\n" + "="*40)
    print("   ZERO-KNOWLEDGE IDENTITY SCANNER")
    print("="*40)
    print("TARGET PERSONA:  Alice")
    print("TRUE DOB:        1990")
    print("CURRENT YEAR:    2026")
    print("REQUIRED AGE:    > 21")
    print("-" * 40)
    
    print("Options:")
    print(" [1] Scan Valid ID (Be Honest)")
    print(" [2] Tamper with Chip (Lie / Fake DOB)")
    
    choice = input("\n>> Select Action (1/2): ")
    
    if choice == '2':
        print_slow("\n...INITIATING TAMPER PROTOCOL...")
        fake_dob = input(">> Enter FAKE Year of Birth (e.g. 2010): ")
        try:
            return int(fake_dob)
        except ValueError:
            print("Invalid input. Defaulting to 1990.")
            return 1990
    else:
        print_slow("\n...SCANNING ID CHIP...")
        return 1990

def id_card_circuit():
    # --- STEP 1: DEFINE CIRCUIT ---
    circuit = FlatCircuit()
    
    # Define wires
    current_year = "2026"
    dob = "dob"          # Renamed to generic 'dob' for variable input
    threshold = "21"
    
    # Circuit Logic: 
    # 1. Calculate Age
    age = circuit.sub(current_year, dob, output_name="age")
    # 2. Check Threshold (Age - 21)
    result = circuit.sub(age, threshold, output_name="result")
    
    # --- STEP 2: COMPILE R1CS ---
    # We only do this once! The rules don't change, only the data does.
    r1cs = R1CS(circuit)
    
    # --- STEP 3: INTERACTIVE INPUT ---
    user_dob = get_user_input()
    
    input_data = {
        "2026": 2026,
        "dob": user_dob, # The user's chosen input
        "21": 21
    }
    
    # --- STEP 4: WITNESS & VERIFY ---
    print_slow("\n>>> GENERATING ZK-PROOF WITNESS...")
    wg = WitnessGenerator(circuit, r1cs)
    w = wg.generate(input_data)
    
    print("\n>>> VERIFYING CONSTRAINTS ON-CHAIN...")
    time.sleep(1)
    
    verified = True
    for i in range(len(r1cs.A)):
        # Dot product: (Row A * w) * (Row B * w) = (Row C * w)
        a_val = sum(r1cs.A[i][j] * w[j] for j in range(len(w)))
        b_val = sum(r1cs.B[i][j] * w[j] for j in range(len(w)))
        c_val = sum(r1cs.C[i][j] * w[j] for j in range(len(w)))
        
        check = (a_val * b_val) - c_val
        
        if check != 0:
            verified = False
            print(f" [x] Constraint {i} FAILED: {a_val} * {b_val} != {c_val}")
    
    print("-" * 40)
    # LOGIC CHECK: 
    # In this simple arithmetic circuit, we check two things:
    # 1. Did the math validly execute? (Constraints Passed)
    # 2. Is the result positive? (Logic Check)
    # Note: In a real SNARK, positivity is a constraint. Here, we check the output value.
    
    result_idx = r1cs.var_map["result"]
    result_value = w[result_idx]
    
    if verified and result_value > 0:
        print(f" ACCESS GRANTED. (Age Check: +{result_value})")
        print(" The Prover honestly computed they are over 21.")
    elif verified and result_value <= 0:
        print(f" ACCESS DENIED. (Age Check: {result_value})")
        print(" The Prover honestly computed they are UNDERAGE.")
    else:
        print(" CRITICAL ERROR: PROOF INVALID.")
        print(" The math does not check out. The Prover is lying about the calculation.")

if __name__ == "__main__":
    id_card_circuit()