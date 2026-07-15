class Top:
    def print(self):
        print("Top")


class A(Top):
    def print(self):
        print("A")
        super().print()


class B(Top):
    def print(self):
        print("B")
        super().print()


class C(A, B):
    pass


class D(B, A):
    pass


if __name__ == "__main__":
    a = A()
    a.print()
    print("---")
    b = B()
    b.print()
    print("---")
    c = C()
    c.print()
    print("---")
    d = D()
    d.print()
