import time
import db
import os

duration = os.environ.get('water_duration')

def water(duration):
    yes_votes, no_votes = db.get_vote_counts()

    if yes_votes == None or no_votes == None:   # DB Connection failure.
        print("DB Connection failed. Using backup watering schedule.")
        # TODO: create backup watering schedule rule. Replace next line
        should_water = False
    else:   # Collected votes successfully
        if yes_votes > no_votes:
            should_water = True
        else:
            should_water = False
    
    if should_water:
        # TODO: Turn on water pump relay
        # Sleep for <duration> seconds
        time.sleep(duration)
        # TODO: Turn off water pump relay
        db.add_water_record()

if __name__ == "__main__":
    water(duration)