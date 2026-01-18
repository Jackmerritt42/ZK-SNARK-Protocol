import sys
import time
from src.circuit import FlatCircuit
from src.r1cs import R1CS
from src.witness import WitnessGenerator
from src.finite_field import FieldElement

# A standard large prime used in examples (or use the BN128 scalar field)
PRIME = 21888242871839275222246405745257275088548364400416034343698204186575808495617

def to_field(num):
    """Helper to convert int -> FieldElement"""
    return FieldElement(num, PRIME)

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
    circuit = FlatCircuit()
    
    current_year = "2026"
    dob = "dob"
    threshold = "21"
    
    # Logic (Remains the same!)
    age = circuit.sub(current_year, dob, output_name="age")
    result = circuit.sub(age, threshold, output_name="result")
    
    # Compile
    r1cs = R1CS(circuit)
    
    # Get Input
    user_dob_int = get_user_input()
    
    # We wrap inputs in FieldElements. The entire circuit will now
    # automatically execute using Modular Arithmetic.
    input_data = {
        "2026": to_field(2026),
        "dob": to_field(user_dob_int),
        "21": to_field(21)
    }
    
    print_slow("\n>>> COMPUTING OVER FINITE FIELD (Modulo P)...")
    wg = WitnessGenerator(circuit, r1cs)
    w = wg.generate(input_data)
    
    # Verify
    print("\n>>> VERIFYING CONSTRAINTS...")
    verified = True
    for i in range(len(r1cs.A)):
        # Calculate dot products using field arithmetic
        # (Since w contains FieldElements, sum() and * work automatically)
        a_val = sum(r1cs.A[i][j] * w[j] for j in range(len(w)))
        b_val = sum(r1cs.B[i][j] * w[j] for j in range(len(w)))
        c_val = sum(r1cs.C[i][j] * w[j] for j in range(len(w)))
        
        check = (a_val * b_val) - c_val
        
        # Check if result is 0 (modulo P)
        if check.value != 0:
            verified = False
            print(f" [x] Constraint {i} FAILED")

    print("-" * 40)
    
    # Check Result
    result_idx = r1cs.var_map["result"]
    result_val = w[result_idx].value
    
    # Note: In Finite Fields, "Negative" numbers look like Huge Positive numbers.
    # e.g. -1 % 7 = 6.
    # So we check if the number is "small positive" or "huge (negative)".
    half_prime = PRIME // 2
    
    if verified:
        if result_val < half_prime:
            print(f" ACCESS GRANTED. (Proof Valid, Age Check: +{result_val})")
        else:
            print(f" ACCESS DENIED. (Proof Valid, Age Check: Negative/Underage)")
    else:
        print(" CRITICAL ERROR: PROOF INVALID.")

if __name__ == "__main__":
    id_card_circuit()