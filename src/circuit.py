class FlatCircuit:
    """
    Represents an Arithmetic Circuit that records operations
    to later be converted into R1CS (Rank-1 Constraint System).
    """
    def __init__(self):
        self.operations = [] # List of {'left', 'right', 'output', 'op'}
        self.variable_counter = 1 # Start at 1 (0 is usually reserved for the constant '1')
        self.one = 'one' # Represents the constant 1

    def allocate(self, name=None):
        """Allocates a new variable (wire) in the circuit."""
        var_name = name if name else f"v{self.variable_counter}"
        self.variable_counter += 1
        return var_name

    def add(self, left, right, output_name=None):
        """Records an Addition gate: left + right = output"""
        out = self.allocate(output_name)
        self.operations.append({
            'left': left,
            'right': right,
            'output': out,
            'op': 'ADD'
        })
        return out

    def sub(self, left, right, output_name=None):
        """Records a Subtraction (basically Addition with neg): left - right = output"""
        # For simplicity in R1CS, we often treat this just like add, or handle constants.
        # Here we just record it as SUB for the flattener to handle.
        out = self.allocate(output_name)
        self.operations.append({
            'left': left,
            'right': right,
            'output': out,
            'op': 'SUB'
        })
        return out

    def mul(self, left, right, output_name=None):
        """Records a Multiplication gate: left * right = output"""
        out = self.allocate(output_name)
        self.operations.append({
            'left': left,
            'right': right,
            'output': out,
            'op': 'MUL'
        })
        return out

    def print_circuit(self):
        print("--- Arithmetic Circuit ---")
        for op in self.operations:
            print(f"{op['output']} = {op['left']} {op['op']} {op['right']}")
        print("--------------------------")