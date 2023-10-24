import concurrent.futures
import json
import requests
import os

from model.timing_model import ReconstructTiming

from utils.fetcher import fetch
from utils.input_handler import get_input
from utils.output_handler import createFilename, write

from .parameters import (ALGORITHMS, NUMBER_OF_OBJECTS, RECONSTRUCT_URL, SIZES,
                         THREAD_COUNT, RECONSTRUCT_TEMP_OUTPUT_PATH)


class Reconstructer:
    def __init__(self, n, k, keys):
        self.n = n
        self.k = k
        self.keys = keys

    def run_test(self):
        for size in SIZES:
            INPUT_FILE_NAME = f"{size}kB_{NUMBER_OF_OBJECTS}objects_dataset_{self.n}-{self.k}_to_reconstruct.json"
            data = get_input(INPUT_FILE_NAME)

            for thread_number in THREAD_COUNT:
                results = []

                with concurrent.futures.ThreadPoolExecutor(thread_number) as executor:
                    with requests.Session() as session:
                        for i in range(thread_number):
                            future = executor.submit(
                                Reconstructer.get_timings, data, f"Thread-{i + 1}", self.keys, session)

                            file = RECONSTRUCT_TEMP_OUTPUT_PATH + \
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
    def get_timings(data, thread, keys, session):
        timings = []

        for algorithm in ALGORITHMS:
            filteredObjects = Reconstructer.filterObjects(data, algorithm)

            for key_number in keys:
                for i, json_object in enumerate(filteredObjects):
                    body = Reconstructer.get_request_body(
                        json_object, algorithm, key_number)
                    single_object_timings = [
                        fetch(body, RECONSTRUCT_URL, session) for j in range(5)]
                    timings.append(ReconstructTiming(
                        algorithm, thread, (i + 1), single_object_timings, key_number))

        return timings

    @staticmethod
    def filterObjects(data, algorithm):
        if algorithm == "shamir":
            return list(filter(lambda json_object: "macKeys" not in json_object and "encKeys" not in json_object and "modulus" not in json_object, data))
        elif algorithm == "pss":
            return list(filter(lambda json_object: "macKeys" in json_object, data))
        elif algorithm == "css":
            return list(filter(lambda json_object: "fingerprints" in json_object, data))
        elif algorithm == "krawczyk":
            return list(filter(lambda json_object: "fingerprints" not in json_object and "encKeys" in json_object and "macKeys" not in json_object, data))
        else:
            return list(filter(lambda json_object: "modulus" in json_object, data))

    @staticmethod
    def get_request_body(json_object, algorithm, key_number):
        copy_json_object = json_object

        toChange = ["shares"]

        if algorithm == "pss":
            toChange.append("macKeys")
            toChange.append("macs")

        if algorithm == "css":
            toChange.append("fingerprints")
            toChange.append("encKeys")

        if algorithm == "krawczyk":
            toChange.append("encKeys")

        for key in toChange:
            for object in copy_json_object[key]:
                if object["index"] > key_number:
                    copy_json_object[key].remove(object)

        if algorithm == "pss":
            innerChanges = ["macKeys", "macs"]

            for key in innerChanges:
                for object in copy_json_object[key]:
                    for innerObject in object["array"]:
                        if innerObject["index"] > key_number:
                            object["array"].remove(innerObject)

        return '{ "secret": ' + json.dumps(copy_json_object) + '}'

    def writeResults(self, size, thread_number, results):
        for algorithm in ALGORITHMS:
            for result in results:
                filteredResults = list(
                    filter(lambda result_object: result_object.algorithm == algorithm, result))
                filename = createFilename(
                    "reconstruct", algorithm, f"{self.n}-{self.k}", size, thread_number, NUMBER_OF_OBJECTS)
                write(filename, filteredResults)
