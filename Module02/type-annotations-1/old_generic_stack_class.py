from typing import Generic, TypeVar


# Pre python 3.12 syntax for generics
T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._contents: list[T] = []

    def push(self, value: T) -> None:
        self._contents.append(value)

    def pop(self) -> T:
        top: T = self._contents[0]
        self._contents = self._contents[1:]
        return top


def main() -> None:
    s1: Stack[int] = Stack()
    s1.push(1)
    s1.push(2)
    print(s1.pop())
    print(s1.pop())

    s2: Stack[str] = Stack()
    s2.push("hello")
    s2.push("world")
    print(s2.pop())
    print(s2.pop())


if __name__ == "__main__":
    main()
