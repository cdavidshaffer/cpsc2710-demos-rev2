def factorial():
    i = 1
    value = 1
    while True:
        yield value
        value *= i
        i += 1