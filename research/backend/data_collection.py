import numpy as np
import threading


class MultiThreading:

    def __init__(self, threads, iteration_list, output: list):
        self.threads = threads
        self.output = output
        self.iteration_list = iteration_list

    def multi_thread_compile(self, thread_count, function):

        """a function that compiles an iteration list to prepare
        multi threadding"""

        jobs = []

        # distribute iteration list to batches and append to jobs list
        batches = [i.tolist() for i in np.array_split(self.iteration_list, thread_count)]

        for i in range(len(batches)):
            jobs.append(threading.Thread(target=function, args=[batches[i]]))

        return jobs

    def multi_thread_execute(self, jobs):

        """executes the multi-threading loop"""

        # Start the threads
        for j in jobs:
            j.start()

        # Ensure all of the threads have finished
        for j in jobs:
            j.join()
        return

    def Run(self, function):

        self.jobs = self.multi_thread_compile(self.threads, function)
        self.multi_thread_execute(self.jobs)
