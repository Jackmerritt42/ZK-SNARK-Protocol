import numpy as np

class WitnessGenerator:
    def __init__(self, circuit, r1cs):
        self.circuit = circuit
        self.r1cs = r1cs
        # Start with the constant 'one': 1
        self.values = {circuit.one: 1}

    def generate(self, input_map):
        """
        Takes a dictionary of initial values (e.g., {'1990': 1990})
        and computes the full witness vector.
        """
        # 1. Load the initial inputs (Private & Public)
        self.values.update(input_map)

        # 2. Re-run the circuit logic to find intermediate values
        print(">>> Computing Trace...")
        for op in self.circuit.operations:
            # Fetch values for left and right inputs
            val_left = self.values[op['left']]
            val_right = self.values[op['right']]
            
            # Compute the output based on the op
            if op['op'] == 'ADD':
                res = val_left + val_right
            elif op['op'] == 'SUB':
                res = val_left - val_right
            elif op['op'] == 'MUL':
                res = val_left * val_right
            else:
                raise ValueError(f"Unknown Op: {op['op']}")
            
            # Store the result
            self.values[op['output']] = res
            print(f"    {op['left']}({val_left}) {op['op']} {op['right']}({val_right}) -> {op['output']}({res})")

        # 3. Flatten into a Vector (ordered by R1CS var_map)
        witness_vec = [0] * self.r1cs.num_vars
        for var_name, idx in self.r1cs.var_map.items():
            if var_name in self.values:
                witness_vec[idx] = self.values[var_name]
            else:
                 raise ValueError(f"Error: Variable '{var_name}' was never computed!")
                 
        return np.array(witness_vec)