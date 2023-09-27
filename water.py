import time
from scripts import db
import os
from datetime import datetime
import automationhat

# Get water duration in seconds, or default to 1.5 seconds:
duration = os.getenv('water_duration', 1.5)

# Get backup watering schedule in days, or default to every 3 days:
backup_water_interval = os.getenv('backup_water_interval', 3)

def water(duration):
    yes_votes, no_votes = db.get_vote_counts(-1)

    if yes_votes == None or no_votes == None:   # DB Connection failure.
        # Use backup watering schedule (Water every <backup_water_interval> days):
        print("DB Connection failed. Using backup watering schedule.")
        day_int = int(datetime.now().weekday())
        if day_int % backup_water_interval == 0:
            should_water = True
        else:
            should_water = False

    else:   # Collected votes successfully
        if yes_votes > no_votes:
            should_water = True
        else:
            should_water = False
    
    if should_water:
        print("Watering the plant")
        automationhat.relay.one.on()
        # Sleep for <duration> seconds
        time.sleep(duration)
        automationhat.relay.one.off()
        db.add_water_record()

if __name__ == "__main__":
    water(duration)
