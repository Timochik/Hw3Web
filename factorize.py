import multiprocessing

def factorize_sync(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(number):
    def worker(num, queue):
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        queue.put(factors)

    processes = []
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    num_cores = multiprocessing.cpu_count()
    chunk_size = number // num_cores

    for i in range(num_cores):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_cores - 1 else number
        p = multiprocessing.Process(target=worker, args=(number, queue))
        processes.append(p)

    try:
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        results = [queue.get() for _ in range(num_cores)]
        return [item for sublist in results for item in sublist]

    except Exception as e:
        print("Error occurred:", e)
        return []

def factorize(*numbers):
    results = []
    for number in numbers:
        try:
            results.append(factorize_sync(number))
        except Exception as e:
            print("Error occurred:", e)
            results.append([])  # Append an empty list if an error occurs
    return results

a, b, c, d = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
