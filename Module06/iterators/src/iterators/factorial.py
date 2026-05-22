class Factorial:
    def __init__(self):
        self.n = 1
        self.current_factorial = 1

    def __iter__(self):
        """Note: All Iterators are Iterable so we must have this method."""
        return self

    def __next__(self):
        result = self.current_factorial
        self.current_factorial *= self.n
        self.n += 1
        return result


if __name__ == "__main__":
    for value in Factorial():
        if value > 1_000_000:
            break
        print(value)

# Output:
# 1
# 1
# 2
# 6
# 24
# 120
# 720
# 5040
# 40320
# 362880
