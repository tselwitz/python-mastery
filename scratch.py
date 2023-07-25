import sys
import time


def parse_line(line: str) -> tuple:
    strs = line.split("=")
    if len(strs) == 2:
        return (strs[0], strs[1])
    return None


def do_work(x, y, fut):
    fut.set_result(worker(x, y))


def worker(x, y):
    print('About to work')
    time.sleep(2)
    print('Done')
    return x + y


if __name__ == "__main__":
    if sys.argv[1] == "1":
        name, val = parse_line("todd=cool")
        print(name)
        print(val)
    if sys.argv[1] == "2":
        import threading
        from concurrent.futures import Future
        fut = Future()
        t = threading.Thread(target=do_work, args=(2, 3, fut))
        t.start()
        result = fut.result()
        print(result)
