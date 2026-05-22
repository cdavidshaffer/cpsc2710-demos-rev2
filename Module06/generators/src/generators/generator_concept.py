def f():
    print(1)
    yield "monkey"
    print(2)
    yield "banana"


if __name__ == '__main__':
    g = f()
    value = next(g)
    print(value)
    value = next(g)
    print(value)
    value = next(g)