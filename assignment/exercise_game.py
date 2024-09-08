"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json


N: int = 10  # number of flashes
sample_ms = 10.0
on_ms = 500


def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # let user know game started / is over
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file."""
    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if t_good:
        avg_response_time = sum(t_good) / len(t_good)
        min_response_time = min(t_good)
        max_response_time = max(t_good)
    else:
        avg_response_time = min_response_time = max_response_time = None

    print(f"Average response time: {avg_response_time} ms")
    print(f"Minimum response time: {min_response_time} ms")
    print(f"Maximum response time: {max_response_time} ms")

    score = (len(t_good) / len(t)) if t else 0.0

    # store results
    data = {
        "average_response_time_ms": avg_response_time,
        "min_response_time_ms": min_response_time,
        "max_response_time_ms": max_response_time,
        "misses": misses,
        "score": score,
        "responses": t,
    }

    # make dynamic filename and write JSON
    now: tuple[int] = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)
    write_json(filename, data)


if __name__ == "__main__":
    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()
        tic = time.ticks_ms()
        t0 = None

        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)
        led.low()

    blinker(5, led)

    scorer(t)
