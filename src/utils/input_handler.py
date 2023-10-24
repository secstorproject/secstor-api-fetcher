import inspect
import json
import os.path

from .parameters import RECONSTRUCT_INPUT_PATH, SPLIT_INPUT_PATH


def get_input(filename):
    frame = inspect.stack()[1].filename
    caller = os.path.splitext(os.path.basename(frame))[0]

    path = (SPLIT_INPUT_PATH + filename) if caller.__contains__("splitter") else (RECONSTRUCT_INPUT_PATH + filename)

    if os.path.exists(path):
        with open(path, 'r') as reader:
            data = reader.read()
    else:
        raise FileNotFoundError(f"{filename} was not found!")
    
    return json.loads(data)
