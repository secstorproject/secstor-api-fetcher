import json
import os
import csv
from itertools import chain
from model.timing_model import SplitTiming, ReconstructTiming
from utils.parameters import (N, K, RECONSTRUCT_OUTPUT_PATH, RECONSTRUCT_TEMP_OUTPUT_PATH, SPLIT_OUTPUT_PATH,
                              THREAD_COUNT, SPLIT_TEMP_OUTPUT_PATH, SIZES, NUMBER_OF_OBJECTS, ALGORITHMS, SPLIT_HEADER, RECONSTRUCT_HEADER)


def main():
    for thread_number in THREAD_COUNT:
        for operation in ["split", "reconstruct"]:
            for size in SIZES:
                if operation == "split":
                    alldata = list(chain.from_iterable([get_file_data(get_file(
                        SPLIT_TEMP_OUTPUT_PATH, size, thread_number, (i + 1)), operation) for i in range(thread_number)]))
                else:
                    alldata = list(chain.from_iterable([get_file_data(get_file(
                        RECONSTRUCT_TEMP_OUTPUT_PATH, size, thread_number, (i + 1)), operation) for i in range(thread_number)]))

                for algorithm in ALGORITHMS:
                    rows = list(
                        filter(lambda x: x.algorithm == algorithm, alldata))

                    file = createFilename(
                        operation, algorithm, f"{N}-{K}", size, thread_number)

                    if operation == "split":
                        path = SPLIT_OUTPUT_PATH + file
                        header = SPLIT_HEADER
                    else:
                        path = RECONSTRUCT_OUTPUT_PATH + file
                        header = RECONSTRUCT_HEADER

                    if os.path.exists(path):
                        os.remove(path)

                    with open(path, 'w', newline='', encoding='utf8') as file:
                        writer = csv.writer(file, delimiter=';')

                        writer.writerow(header)

                        for row_object in rows:
                            row = [row_object.thread, row_object.register]

                            if operation == "reconstruct":
                                row.append(row_object.keys)

                            for timing in row_object.timings:
                                row.append(str(timing))

                            writer.writerow(row)


def as_split_timing(obj):
    return SplitTiming(obj["algorithm"], obj["thread"], obj["register"], obj["timings"])


def as_reconstruct_timing(obj):
    return ReconstructTiming(obj["algorithm"], obj["thread"], obj["register"], obj["timings"], obj["keys"])


def get_file(path, size, thread_number, current_thread):
    return f"{path}temp_{N}-{K}_{size}kb_{thread_number}_Thread-{current_thread}_{NUMBER_OF_OBJECTS}objects.json"


def get_file_data(file, operation):
    if operation == "split":
        with open(file) as jsonFile:
            data = json.load(jsonFile, object_hook=as_split_timing)
    else:
        with open(file) as jsonFile:
            data = json.load(jsonFile, object_hook=as_reconstruct_timing)

    return data


def createFilename(operation, algorithm, parameters, size, thread_count):
    thread = (str(thread_count) +
              "threads") if thread_count > 1 else (str(thread_count) + "thread")

    return f"{operation}_{algorithm}_{parameters}_{size}kB_{thread}_{str(NUMBER_OF_OBJECTS)}objects.csv"


main()
