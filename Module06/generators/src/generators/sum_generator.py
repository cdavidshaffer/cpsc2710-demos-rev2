class ResetSum(Exception):
    pass

def sum_generator():
    total = 0
    while True:
        try:
            x = yield total
            total += x
        except ResetSum:
            total = 0
