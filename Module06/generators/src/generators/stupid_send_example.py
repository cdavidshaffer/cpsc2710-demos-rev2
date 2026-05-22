def f():
    print("f is about to yield")
    x = yield 1
    print(f"f returned from yield with {x=}")
    yield 2

if __name__ == "__main__":
    g = f()
    print("calling send")
    z = g.send(None)
    print(f"send returned with {z=}")
    print("calling send")
    z = g.send(99)
    print(f"{z=}")