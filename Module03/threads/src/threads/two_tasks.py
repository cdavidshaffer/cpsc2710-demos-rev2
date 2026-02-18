import threading
import time


def task_a():
    for i in range(0, 10):
        time.sleep(1)
        print(i)


def task_b():
    for i in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
        time.sleep(1)
        print(i)


def main_sequential():
    task_a()
    task_b()


def main_threaded():
    thread_a = threading.Thread(target=task_a)
    thread_a.start()
    task_b()
    thread_a.join()
