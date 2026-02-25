import time
from threading import Thread


def task_a():
    for i in range(0, 20):
        time.sleep(0.5)
        print(i)


def task_b():
    for i in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
        time.sleep(0.5)
        print(i)


def task_c():
    for i in ["k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]:
        time.sleep(0.5)
        print(i)


def main_sequential():
    task_a()
    task_b()


def main_threaded():
    thread_a = Thread(target=task_a)
    thread_a.start()
    thread_c = Thread(target=task_c)
    thread_c.start()

    task_b()
    thread_a.join()
    thread_c.join()


if __name__ == "__main__":
    main_threaded()
