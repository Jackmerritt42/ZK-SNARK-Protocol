import numpy as np

class R1CS:
    def __init__(self, flat_circuit):
        self.circuit = flat_circuit
        self.var_map = {} # Maps variable names "v1" -> index 0, 1, 2...
        self.A = []
        self.B = []
        self.C = []
        
        self._build_var_map()
        self._compile_constraints()

    def _build_var_map(self):
        """
        Assigns a unique index to every variable in the circuit.
        Index 0 is always reserved for the constant 'one'.
        """
        # 1. Start with the constant 'one'
        variables = set([self.circuit.one])
        
        # 2. Collect all used variables from operations
        for op in self.circuit.operations:
            variables.add(op['left'])
            variables.add(op['right'])
            variables.add(op['output'])
            
        # 3. Create the map
        # Sort them to ensure deterministic order (important for verifying later!)
        sorted_vars = sorted(list(variables))
        # Ensure 'one' is at index 0
        if self.circuit.one in sorted_vars:
            sorted_vars.remove(self.circuit.one)
            sorted_vars.insert(0, self.circuit.one)
            
        for i, var in enumerate(sorted_vars):
            self.var_map[var] = i
            
        self.num_vars = len(self.var_map)
        print(f"Variable Mapping: {self.var_map}")

    def _get_vector(self, variable_name):
        """Creates a vector of size N with a 1 at the variable's index."""
        vec = [0] * self.num_vars
        if variable_name in self.var_map:
            idx = self.var_map[variable_name]
            vec[idx] = 1
        return vec
        
    def _compile_constraints(self):
        """
        Converts each operation into A * B = C vectors.
        """
        for op in self.circuit.operations:
            # Initialize empty vectors for this constraint
            a_vec = [0] * self.num_vars
            b_vec = [0] * self.num_vars
            c_vec = [0] * self.num_vars
            
            # Get indices
            left_idx = self.var_map[op['left']]
            right_idx = self.var_map[op['right']]
            out_idx = self.var_map[op['output']]
            one_idx = self.var_map[self.circuit.one]

            if op['op'] == 'MUL':
                # Logic: left * right = output
                # A: [left], B: [right], C: [output]
                a_vec[left_idx] = 1
                b_vec[right_idx] = 1
                c_vec[out_idx] = 1
            
            elif op['op'] == 'ADD':
                # Logic: (left + right) * 1 = output
                # A: [left, right], B: [one], C: [output]
                a_vec[left_idx] = 1
                a_vec[right_idx] = 1
                b_vec[one_idx] = 1
                c_vec[out_idx] = 1

            elif op['op'] == 'SUB':
                # Logic: (left - right) * 1 = output
                # A: [left, -right], B: [one], C: [output]
                a_vec[left_idx] = 1
                a_vec[right_idx] = -1 # Negative!
                b_vec[one_idx] = 1
                c_vec[out_idx] = 1
            
            self.A.append(a_vec)
            self.B.append(b_vec)
            self.C.append(c_vec)

    def print_r1cs(self):
        print("\n--- R1CS Constraints (A * B = C) ---")
        for i in range(len(self.A)):
            print(f"Constraint {i+1}:")
            print(f"  A: {self.A[i]}")
            print(f"  B: {self.B[i]}")
            print(f"  C: {self.C[i]}")