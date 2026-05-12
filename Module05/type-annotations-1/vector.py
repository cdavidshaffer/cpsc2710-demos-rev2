# For Python 3.8 to 3.13 you must include this to permit forward references
# from __future__ import annotations
# Prior to Python 3.8 you must use string literals for forward references.  See comment below.


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # Note: Vector is a "forward reference" as the Vector class has not been completely defined yet.
    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float) -> Vector:
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> Vector:
        return Vector(self.x * other, self.y * other)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


def main() -> None:
    v1: Vector = Vector(12, 2)
    v2: Vector = Vector(10, 25)
    print(v1 + v2)
    print(v1 * 5)
    print(5 * v1)


if __name__ == "__main__":
    main()
