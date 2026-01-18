from src.finite_field import FieldElement
from src.polynomial import lagrange_interpolation, Polynomial

PRIME = 21888242871839275222246405745257275088548364400416034343698204186575808495617

def to_field(num):
    return FieldElement(num, PRIME)

# Points: (1, 3), (2, 2), (3, 4)
# We want a curve that hits these exact spots.
xs = [to_field(1), to_field(2), to_field(3)]
ys = [to_field(3), to_field(2), to_field(4)]

poly = lagrange_interpolation(xs, ys, PRIME)

print("Polynomial:", poly)
print("f(1) =", poly.evaluate(1)) # Should be 3
print("f(2) =", poly.evaluate(2)) # Should be 2
print("f(3) =", poly.evaluate(3)) # Should be 4