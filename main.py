from src.circuit import FlatCircuit
from src.r1cs import R1CS

def id_card_circuit():
    circuit = FlatCircuit()
    
    print(">>> 1. Compiling Circuit...")
    current_year = "2026"
    dob = "1990"
    
    # Operations
    age = circuit.sub(current_year, dob, output_name="age")
    threshold = "21"
    result = circuit.sub(age, threshold, output_name="result")
    
    circuit.print_circuit()
    
    print(">>> 2. Generating R1CS...")
    r1cs = R1CS(circuit)
    r1cs.print_r1cs()
    
    # Optional: Verify it works with our witnessing data
    # (We will build the 'Witness' generator next!)

if __name__ == "__main__":
    id_card_circuit()