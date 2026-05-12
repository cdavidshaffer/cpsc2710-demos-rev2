def bad(names=[]):
    print(names)
    names.append("Mark")
    print(names)


def main():
    bad()  # [], [Mark]
    bad()  # [], [Mark]


if __name__ == "__main__":
    main()
