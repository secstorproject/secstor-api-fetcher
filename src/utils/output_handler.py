import csv
import inspect
import os.path

from .parameters import (RECONSTRUCT_HEADER, RECONSTRUCT_OUTPUT_PATH,
                         SPLIT_HEADER, SPLIT_OUTPUT_PATH)


def write(filename, rows):
    frame = inspect.stack()[1].filename
    caller = os.path.splitext(os.path.basename(frame))[0]

    if caller.__contains__("splitter"):
        path = SPLIT_OUTPUT_PATH + filename
        header = SPLIT_HEADER
    else:
        path = RECONSTRUCT_OUTPUT_PATH + filename
        header = RECONSTRUCT_HEADER

    method = 'a' if os.path.exists(path) else 'w'

    with open(path, method, newline='', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';')

        if method == 'w':
            writer.writerow(header)

        for row_object in rows:
            row = [row_object.thread, row_object.register]

            if caller.__contains__("reconstructer"):
                row.append(row_object.keys)

            for timing in row_object.timings:
                row.append(str(timing))

            writer.writerow(row)


def createFilename(operation, algorithm, parameters, size, thread_count, object_count):
    thread = (str(thread_count) +
              "threads") if thread_count > 1 else (str(thread_count) + "thread")

    return f"{operation}_{algorithm}_{parameters}_{size}kB_{thread}_{str(object_count)}objects.csv"
