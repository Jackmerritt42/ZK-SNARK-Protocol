class FieldElement:
    def __init__(self, value, prime):
        self.value = value % prime
        self.prime = prime

    def __add__(self, other):
        if isinstance(other, FieldElement):
            val = other.value
        elif isinstance(other, int):
            val = other
        else:
            return NotImplemented
        return FieldElement((self.value + val) % self.prime, self.prime)

    def __sub__(self, other):
        if isinstance(other, FieldElement):
            val = other.value
        elif isinstance(other, int):
            val = other
        else:
            return NotImplemented
        # Ensure result is positive
        return FieldElement((self.value - val) % self.prime, self.prime)

    def __mul__(self, other):
        if isinstance(other, FieldElement):
            val = other.value
        elif isinstance(other, int):
            val = other
        else:
            return NotImplemented
        return FieldElement((self.value * val) % self.prime, self.prime)

    def __truediv__(self, other):
        if isinstance(other, FieldElement):
            val = other.value
        elif isinstance(other, int):
            val = other
        else:
            return NotImplemented
        
        # Fermat's Little Theorem: a^(p-2) is the modular inverse of a mod p
        inv = pow(val, self.prime - 2, self.prime)
        return FieldElement((self.value * inv) % self.prime, self.prime)

    def __neg__(self):
        return FieldElement((0 - self.value) % self.prime, self.prime)
        
    def __eq__(self, other):
        if isinstance(other, FieldElement):
            return self.value == other.value and self.prime == other.prime
        elif isinstance(other, int):
            return self.value == (other % self.prime)
        return False

    def __repr__(self):
        return str(self.value)
        
    # Allow (int + FieldElement) to work
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)