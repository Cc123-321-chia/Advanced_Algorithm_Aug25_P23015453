import threading
import time
import math

# =============================================================================
# SECTION 1: Factorial Function
# =============================================================================

def factorial_iterative(n):
    """
    Big-O Analysis:
    T(n) = n * O(1) = O(n)
    """
    if n < 0:
        raise ValueError("Factorial cannot be negative")
    if n == 0 or n == 1:
        return 1

    result = 1
    # Loop n times -> O(n) time complexity
    for i in range(2, n + 1):
        result *= i  # Each loop performs 1 multiplication operation
    return result

# =============================================================================
# SECTION 2: Multithreading Factorial Calculation
# =============================================================================

class FactorialThread(threading.Thread):
    """Thread class for calculating factorial"""

    def __init__(self, number, thread_id, results_dict, execution_times):
        """
        Initialize thread
        number: number to calculate factorial for
        thread_id: thread identifier
        results_dict: dictionary to store results
        execution_times: dictionary to store execution times
        """
        threading.Thread.__init__(self)
        self.number = number
        self.thread_id = thread_id
        self.results_dict = results_dict
        self.execution_times = execution_times
        self.start_time = None
        self.end_time = None

    def run(self):
        """Main thread execution method"""
        # Record start time
        self.start_time = time.time_ns()

        GREEN = '\033[92m'
        BLUE = '\033[94m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'

        if self.thread_id == "T1":
            color = GREEN
        elif self.thread_id == "T2":
            color = BLUE
        elif self.thread_id == "T3":
            color = YELLOW
        else:
            color = RESET

        print(f"{color}{self.thread_id} START ({self.number}!){RESET}")

        # Calculate factorial
        result = factorial_iterative(self.number)

        # Record end time
        self.end_time = time.time_ns()

        # Store results and execution times
        self.results_dict[self.number] = result
        self.execution_times[self.number] = {
            'start': self.start_time,
            'end': self.end_time,
            'thread_id': self.thread_id
        }

        print(f"{color}{self.thread_id} END ({self.number}!){RESET}")

def multithreaded_factorials(numbers):
    """
    Calculate multiple factorials using multithreading
    """
    print("CONCURRENT PROCESSING:")

    # Store results and execution times
    results = {}
    execution_times = {}
    threads = []

    # Create and start threads
    for i, num in enumerate(numbers):
        thread = FactorialThread(num, f"T{i + 1}", results, execution_times)
        threads.append(thread)

    # Record start time before first thread starts
    overall_start_time = time.time_ns()

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Record end time after last thread completes
    overall_end_time = time.time_ns()

    # Calculate actual total execution time
    start_times = [data['start'] for data in execution_times.values()]
    end_times = [data['end'] for data in execution_times.values()]

    first_start = min(start_times)
    last_end = max(end_times)
    actual_total_time = last_end - first_start

    return results, execution_times, actual_total_time, overall_end_time - overall_start_time


# =============================================================================
# SECTION 3: Single-thread Factorial Calculation
# =============================================================================

def singlethreaded_factorials(numbers):
    """
    Calculate multiple factorials using single thread
    """
    print("Starting single-thread calculation...")

    results = {}
    execution_times = {}

    # Record start time
    start_time = time.time_ns()

    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    # Calculate each factorial sequentially
    for i, num in enumerate(numbers):
        thread_id = f"ST{i + 1}"

        # 根据线程ID选择颜色
        if thread_id == "ST1":
            color = GREEN
        elif thread_id == "ST2":
            color = BLUE
        elif thread_id == "ST3":
            color = YELLOW
        else:
            color = RESET

        print(f"{color}{thread_id} START ({num}!){RESET}")
        thread_start = time.time_ns()

        result = factorial_iterative(num)

        thread_end = time.time_ns()
        print(f"{color}{thread_id} END ({num}!){RESET}")

        results[num] = result
        execution_times[num] = {
            'start': thread_start,
            'end': thread_end,
            'thread_id': thread_id
        }

    # Record end time
    end_time = time.time_ns()
    total_time = end_time - start_time

    return results, execution_times, total_time

# =============================================================================
# SECTION 4: Performance Testing and Results Display
# =============================================================================

def format_time_ns(nanoseconds):
    """Format nanoseconds to readable format"""
    if nanoseconds < 1000:
        return f"{nanoseconds} ns"
    elif nanoseconds < 1_000_000:
        return f"{nanoseconds / 1000:.2f} µs"
    elif nanoseconds < 1_000_000_000:
        return f"{nanoseconds / 1_000_000:.2f} ms"
    else:
        return f"{nanoseconds / 1_000_000_000:.2f} s"

def run_multithreading_experiment():
    """Run multithreading experiment (10 rounds)"""
    numbers = [50, 100, 200]
    rounds = 10

    print("=" * 70)
    print(" " * 10 + "Multithreading Factorial Experiment (10 Rounds)")
    print("=" * 70)

    round_times = []

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num} Test:")
        print("-" * 40)

        _, _, actual_time, _ = multithreaded_factorials(numbers)
        round_times.append(actual_time)

        print(f"    This round time: {format_time_ns(actual_time)}")

    # Calculate statistics
    avg_time = sum(round_times) / len(round_times)
    min_time = min(round_times)
    max_time = max(round_times)

    print("\n" + "=" * 70)
    print(" " * 20 + "Results of Multithreading")
    print("=" * 70)
    for i, t in enumerate(round_times, 1):
        print(f"  Round {i:2d}: {t:>15,} ns")

    print("\nSummary:")
    print(f"  Average time   : {format_time_ns(avg_time)}")
    print(f"  Minimum time   : {format_time_ns(min_time)}")
    print(f"  Maximum time   : {format_time_ns(max_time)}")
    print(f"  Time range     : {format_time_ns(max_time - min_time)}")

    return round_times, avg_time


def run_singlethread_experiment():
    """Run single-thread experiment (10 rounds)"""
    numbers = [50, 100, 200]
    rounds = 10

    print("\n" + "=" * 70)
    print(" " * 10 + "Single-thread Factorial Experiment (10 Rounds)")
    print("=" * 70)

    round_times = []

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num} Test:")
        print("-" * 40)

        _, _, total_time = singlethreaded_factorials(numbers)
        round_times.append(total_time)

        print(f"    This round time: {format_time_ns(total_time)}")

    # Calculate statistics
    avg_time = sum(round_times) / len(round_times)
    min_time = min(round_times)
    max_time = max(round_times)

    print("\n" + "=" * 70)
    print(" " * 20 + "Results of Single-thread")
    print("=" * 70)
    for i, t in enumerate(round_times, 1):
        print(f"  Round {i:2d}: {t:>15,} ns")

    print("\nSummary:")
    print(f"  Average time   : {format_time_ns(avg_time)}")
    print(f"  Minimum time   : {format_time_ns(min_time)}")
    print(f"  Maximum time   : {format_time_ns(max_time)}")
    print(f"  Time range     : {format_time_ns(max_time - min_time)}")

    return round_times, avg_time

def compare_results(multi_times, multi_avg, single_times, single_avg):
    """Compare multithreading and single-thread results"""
    print("\n" + "=" * 70)
    print(" " * 20 + "Performance Comparison Analysis")
    print("=" * 70)

    # 先显示表格
    print("\nRound-by-round Comparison:")
    print("  Round | Multithreading Time | Single-thread Time")
    print("-" * 55)
    for i in range(len(multi_times)):
        multi_t = multi_times[i]
        single_t = single_times[i]
        print(f"  {i + 1:2d}    | {format_time_ns(multi_t):>18}  | {format_time_ns(single_t):>16}")

    # Then it displays the average time and performance comparison.
    print(f"\nMultithreading average time : {format_time_ns(multi_avg)}")
    print(f"Single-thread average time    : {format_time_ns(single_avg)}")

    # Determine which is faster and display the performance difference.
    if multi_avg > single_avg:
        print(f"\n -> Single-thread is faster than Multithreading")
    else:
        print(f"\n -> Multithreading is faster than Single-thread")

# =============================================================================
# SECTION 5: Main Program
# =============================================================================

def main():
    """Main program"""
    print("*" * 70)
    print(" " * 15 + "Multithreading VS Single-Threading")
    print("*" * 70)

    # Run experiments
    multi_times, multi_avg = run_multithreading_experiment()
    single_times, single_avg = run_singlethread_experiment()

    # Compare results
    compare_results(multi_times, multi_avg, single_times, single_avg)

    print("\n" + "=" * 70)
    print(" " * 20 + "Experiment Completed !")
    print("=" * 70)

if __name__ == "__main__":
    main()
