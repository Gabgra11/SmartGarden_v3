import time
import os
import automationhat

# Get water duration in seconds, or default to 5 seconds:
duration = os.getenv('water_duration', 1.5)

def water(duration):
    print("Watering the plant")
    automationhat.relay.one.on()
    # Sleep for <duration> seconds
    time.sleep(duration)
    automationhat.relay.one.off()

if __name__ == "__main__":
    water(duration)
