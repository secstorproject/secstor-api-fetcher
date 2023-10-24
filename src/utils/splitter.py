import concurrent.futures
import json
import os
import requests

from model.timing_model import SplitTiming

from .fetcher import fetch
from .input_handler import get_input
from .output_handler import createFilename, write
from .parameters import (ALGORITHMS, NUMBER_OF_OBJECTS, SIZES, SPLIT_URL,
                         THREAD_COUNT, SPLIT_TEMP_OUTPUT_PATH)


class Splitter:
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def run_test(self):
        for size in SIZES:
            INPUT_FILE_NAME = f"{size}kB_{NUMBER_OF_OBJECTS}objects_dataset_to_split.json"
            data = get_input(INPUT_FILE_NAME)

            for thread_number in THREAD_COUNT:
                results = []

                with concurrent.futures.ThreadPoolExecutor(thread_number) as executor:
                    with requests.Session() as session:
                        for i in range(thread_number):
                            future = executor.submit(
                                Splitter.get_timings, data, f"Thread-{i + 1}", session)

                            file = SPLIT_TEMP_OUTPUT_PATH + \
                                f"temp_{self.n}-{self.k}_{size}kB_{thread_number}_Thread-{i + 1}_{NUMBER_OF_OBJECTS}objects.json"

                            if not os.path.exists(file):
                                open(file, 'w').close()
                            else:
                                os.remove(file)
                                open(file, 'w').close()

                            with open(file) as jsonFile:
                                try:
                                    tempData = json.load(jsonFile)
                                except:
                                    tempData = []

                            for result in future.result():
                                tempData.append(result.__dict__)

                            with open(file, 'w') as jsonFile:
                                json.dump(tempData, jsonFile,
                                          ensure_ascii=False, indent=4)

                            results.append(future.result())

                if (thread_number > 1):
                    for result_list in results:
                        result_list.sort(
                            key=lambda result_object: result_object.thread)

                self.writeResults(size, thread_number, results)

    @staticmethod
    def get_timings(data, thread, session):
        timings = []

        for algorithm in ALGORITHMS:
            for i, json_object in enumerate(data):
                body = Splitter.get_request_body(json_object, algorithm)
                single_object_timings = [
                    fetch(body, SPLIT_URL, session) for i in range(5)]
                timings.append(SplitTiming(algorithm, thread,
                               (i + 1), single_object_timings))

        return timings

    @staticmethod
    def get_request_body(dataset_object, algorithm):
        return '{ "data": ' + json.dumps(dataset_object) + ', "algorithm": "' + algorithm + '"}'

    def writeResults(self, size, thread_number, results):
        for algorithm in ALGORITHMS:
            for result in results:
                filteredResults = list(
                    filter(lambda result_object: result_object.algorithm == algorithm, result))
                filename = createFilename(
                    "split", algorithm, f"{self.n}-{self.k}", size, thread_number, NUMBER_OF_OBJECTS)
                write(filename, filteredResults)
