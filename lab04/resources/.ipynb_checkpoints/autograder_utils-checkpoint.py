# autograder_utils.py
import multiprocessing
import hashlib

def process_wrapper(func, args, queue):
    # Wrapper to get any function to test.
    try:
        result = func(*args)
        queue.put(result)
    except Exception as e:
        queue.put(e)

def time_limited_test_mp(func, *args, timeout=2.0, default_value=None):
    # Multiprocess check to take the infinite loops using Mutliprocessing, assuming that any VM could have different CPUs nodes to run the code.
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=process_wrapper, args=(func, args, queue))
    process.start()
    process.join(timeout)
    
    if process.is_alive():
        process.terminate()
        process.join()
        return default_value
        
    if not queue.empty():
        return queue.get()
        
    return default_value

def get_hash(val):
    # Assuming this is your hash function implementation
    return hashlib.md5(str(val).encode('utf-8')).hexdigest()