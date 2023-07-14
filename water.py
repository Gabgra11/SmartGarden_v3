import time
import db
import os

duration = os.environ.get('water_duration')

def water(duration):
    # TODO: Turn on water pump relay
    # Sleep for <duration> seconds
    time.sleep(duration)
    # TODO: Turn off water pump relay
    db.add_water_record()

if __name__ == "__main__":
    water(duration)