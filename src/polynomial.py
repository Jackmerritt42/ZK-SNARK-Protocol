from src.finite_field import FieldElement

class Polynomial:
    def __init__(self, coeffs):
        """
        coeffs: List of FieldElements, starting from x^0.
        [1, 2, 3] -> 1 + 2x + 3x^2
        """
        self.coeffs = coeffs

    def degree(self):
        return len(self.coeffs) - 1

    def __add__(self, other):
        if isinstance(other, Polynomial):
            # Pad the shorter list with zeros
            max_len = max(len(self.coeffs), len(other.coeffs))
            new_coeffs = []
            for i in range(max_len):
                c1 = self.coeffs[i] if i < len(self.coeffs) else 0
                c2 = other.coeffs[i] if i < len(other.coeffs) else 0
                new_coeffs.append(c1 + c2)
            return Polynomial(new_coeffs)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            max_len = max(len(self.coeffs), len(other.coeffs))
            new_coeffs = []
            for i in range(max_len):
                c1 = self.coeffs[i] if i < len(self.coeffs) else 0
                c2 = other.coeffs[i] if i < len(other.coeffs) else 0
                new_coeffs.append(c1 - c2)
            return Polynomial(new_coeffs)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            # Degree of result is deg(A) + deg(B)
            result_len = len(self.coeffs) + len(other.coeffs) - 1
            result_coeffs = [0] * result_len
            
            # Since these are FieldElements, 0 is an int, so we need a FieldElement Zero
            # We grab the prime from the first coefficient for initializing
            prime = self.coeffs[0].prime
            result_coeffs = [FieldElement(0, prime) for _ in range(result_len)]

            for i, c1 in enumerate(self.coeffs):
                for j, c2 in enumerate(other.coeffs):
                    result_coeffs[i+j] = result_coeffs[i+j] + (c1 * c2)
            return Polynomial(result_coeffs)
        return NotImplemented

    def evaluate(self, x):
        """Evaluate P(x) using Horner's Method"""
        if isinstance(x, int):
             # Wrap in FieldElement using the prime of the coefficients
             x = FieldElement(x, self.coeffs[0].prime)
             
        result = FieldElement(0, self.coeffs[0].prime)
        for coeff in reversed(self.coeffs):
            result = (result * x) + coeff
        return result

    def __repr__(self):
        # Pretty print: 3x^2 + 2x + 1
        s = []
        for i, c in enumerate(self.coeffs):
            s.append(f"{c}x^{i}")
        return " + ".join(s)

def lagrange_interpolation(x_points, y_points, prime):
    """
    Given points (x, y), find the lowest degree Polynomial P(x) that passes through them.
    P(x) = Sum( y_i * L_i(x) )
    where L_i(x) is the Lagrange Basis Polynomial.
    """
    # 1. We need a zero polynomial and a one polynomial for accumulation
    total_poly = Polynomial([FieldElement(0, prime)])
    
    for i in range(len(x_points)):
        xi, yi = x_points[i], y_points[i]
        
        # Start constructing L_i(x)
        # Numerator: Product of (x - xj)
        # Denominator: Product of (xi - xj)
        
        numerator = Polynomial([FieldElement(1, prime)])
        denominator = FieldElement(1, prime)
        
        for j in range(len(x_points)):
            if i == j: 
                continue
            xj = x_points[j]
            
            # (x - xj)
            # Poly representation: [-xj, 1] -> -xj + 1x
            term = Polynomial([FieldElement(0, prime) - xj, FieldElement(1, prime)])
            numerator = numerator * term
            
            # (xi - xj)
            denominator = denominator * (xi - xj)
            
        # L_i(x) = numerator / denominator
        # We multiply coefficients by (1/denominator)
        inv_denom = FieldElement(1, prime) / denominator
        
        # Scale the polynomial
        scaled_coeffs = [c * inv_denom for c in numerator.coeffs]
        L_i = Polynomial(scaled_coeffs)
        
        # Add yi * L_i(x) to total
        # We scale L_i by yi
        term_coeffs = [c * yi for c in L_i.coeffs]
        term_poly = Polynomial(term_coeffs)
        
        total_poly = total_poly + term_poly
        
    return total_poly