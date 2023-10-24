import time
from requests import RequestException
from utils.parameters import ERROR_SLEEP_TIME


def fetch(body, URL, session):
    while True:
        try:
            start = time.perf_counter()

            with session.post(url=URL, headers={"Content-Type": "application/json"}, data=body) as response:
                pass

            end = time.perf_counter() - start
            end = float(end * 1000)

            break
        except RequestException as error:
            print(f"Error on request, message: {error}")
            time.sleep(ERROR_SLEEP_TIME)
            print("Trying again...")

    return format(end, '.3f').replace('.', ',')
