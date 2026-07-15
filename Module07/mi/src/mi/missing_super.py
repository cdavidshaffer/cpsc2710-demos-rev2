class A:
    def __init__(self):
        super().__init__()
        self.__x = 99


class B:
    def __init__(self):
        super().__init__()
        self.__y = 5


class C(A, B):
    def __init__(self):
        super().__init__()
        self.__z = 1
