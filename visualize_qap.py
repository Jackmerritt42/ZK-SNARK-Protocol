from src.finite_field import FieldElement
from src.polynomial import lagrange_interpolation, Polynomial

# 1. Setup Field
PRIME = 21888242871839275222246405745257275088548364400416034343698204186575808495617
def to_field(num): return FieldElement(num, PRIME)

def visualize_simple_qap():
    print("--- VISUALIZING QAP (Polynomial Interpolation) ---")
    
    # Imagine we have 3 Constraints (Gates) in our circuit.
    # We assign them x-coordinates: x=1, x=2, x=3.
    xs = [to_field(1), to_field(2), to_field(3)]
    
    # ---------------------------------------------------------
    # SCENARIO: 
    # We want to represent the logic of the Witness Vector 'A'
    # across the whole circuit as ONE curve.
    # ---------------------------------------------------------
    
    # Let's say at Gate 1, the value needed is 3.
    # At Gate 2, the value needed is 2.
    # At Gate 3, the value needed is 4.
    ys = [to_field(3), to_field(2), to_field(4)]
    
    print("1. Generating Curve that hits our Logic Gates...")
    poly = lagrange_interpolation(xs, ys, PRIME)
    print(f"   Polynomial: {poly}")
    
    # VISUAL CHECK:
    # Does the curve actually pass through our gates?
    print("\n2. Checking the 'Graph':")
    for x, target_y in zip(xs, ys):
        actual_y = poly.evaluate(x)
        match = "MATCH" if actual_y == target_y else "MISS"
        print(f"   At x={x}: Target y={target_y} | Actual Curve y={actual_y} -> {match}")
        
    print("\nThis curve IS the proof. Instead of sending the list [3, 2, 4],")
    print("we send the coefficients of this polynomial.")

if __name__ == "__main__":
    visualize_simple_qap()