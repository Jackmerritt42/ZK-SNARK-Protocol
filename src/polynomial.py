from src.finite_field import FieldElement

class Polynomial:
    def __init__(self, coeffs):
        """
        coeffs: List of FieldElements, starting from x^0.
        [1, 2, 3] -> 1 + 2x + 3x^2
        """
        # Strip trailing zeros
        while len(coeffs) > 1 and coeffs[-1].value == 0:
            coeffs.pop()
        self.coeffs = coeffs

    def degree(self):
        return len(self.coeffs) - 1

    def __add__(self, other):
        if isinstance(other, Polynomial):
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
            result_len = len(self.coeffs) + len(other.coeffs) - 1
            # Initialize with proper FieldElement zero
            prime = self.coeffs[0].prime
            result_coeffs = [FieldElement(0, prime) for _ in range(result_len)]

            for i, c1 in enumerate(self.coeffs):
                for j, c2 in enumerate(other.coeffs):
                    result_coeffs[i+j] = result_coeffs[i+j] + (c1 * c2)
            return Polynomial(result_coeffs)
        return NotImplemented

    def __truediv__(self, other):
        """
        Polynomial Long Division. 
        Returns (Quotient, Remainder).
        """
        if isinstance(other, Polynomial):
            quotient = []
            remainder = Polynomial(self.coeffs[:]) # Copy
            divisor = other

            if divisor.degree() < 0: raise ValueError("Divide by Zero Poly")
            if remainder.degree() < divisor.degree():
                # Self is smaller than divisor -> Quotient is 0, Remainder is self
                prime = self.coeffs[0].prime
                return Polynomial([FieldElement(0, prime)]), remainder

            # While remainder is larger than divisor, keep dividing
            while remainder.degree() >= divisor.degree():
                # Lead coeff of remainder / Lead coeff of divisor
                lead_rem = remainder.coeffs[-1]
                lead_div = divisor.coeffs[-1]
                factor = lead_rem / lead_div
                
                # The degree difference
                deg_diff = remainder.degree() - divisor.degree()
                
                # Construct the subtraction term (factor * x^deg_diff)
                prime = remainder.coeffs[0].prime
                term_coeffs = [FieldElement(0, prime)] * deg_diff + [factor]
                term_poly = Polynomial(term_coeffs)
                
                # Update quotient
                # (Ideally we'd accumulate this, but for QAP checks we mostly care about remainder == 0)
                # For this basic implementation, we just need to reduce the remainder.
                
                to_subtract = divisor * term_poly
                remainder = remainder - to_subtract
                
            # Note: We are not tracking the full quotient list here to keep it simple
            # We strictly need Remainder to be Zero for the proof check.
            return None, remainder 
            
        return NotImplemented

    def evaluate(self, x):
        """Evaluate P(x) using Horner's Method"""
        if isinstance(x, int):
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
        return " + ".join(s) if s else "0"

def lagrange_interpolation(x_points, y_points, prime):
    """
    Given points (x, y), find the lowest degree Polynomial P(x) that passes through them.
    P(x) = Sum( y_i * L_i(x) )
    """
    total_poly = Polynomial([FieldElement(0, prime)])
    
    for i in range(len(x_points)):
        xi, yi = x_points[i], y_points[i]
        
        numerator = Polynomial([FieldElement(1, prime)])
        denominator = FieldElement(1, prime)
        
        for j in range(len(x_points)):
            if i == j: continue
            xj = x_points[j]
            
            # (x - xj)
            term = Polynomial([FieldElement(0, prime) - xj, FieldElement(1, prime)])
            numerator = numerator * term
            denominator = denominator * (xi - xj)
            
        inv_denom = FieldElement(1, prime) / denominator
        scaled_coeffs = [c * inv_denom for c in numerator.coeffs]
        L_i = Polynomial(scaled_coeffs)
        
        # Add yi * L_i(x)
        term_coeffs = [c * yi for c in L_i.coeffs]
        total_poly = total_poly + Polynomial(term_coeffs)
        
    return total_poly