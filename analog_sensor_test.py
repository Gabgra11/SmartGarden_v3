import automationhat
import time

def analog_reading_to_percent(val):
    dry = 2.5
    wet = 0.8

    result = (val-dry)/(wet-dry)*(100)

    if result > 100.0:
        print("Result greater than 100: ", result)
        result = 100.0

    if result < 0:
        print("Result less than 0: ", result)
        result = 0

    return result

def truncate(val, decimals):
    return int(val * (10**decimals))/(10**decimals)

def read_stats():
    moisture_reading = automationhat.analog.one.read()
    moisture = analog_reading_to_percent(moisture_reading)
    moisture = truncate(moisture, 1)
    print("Moisture: ", moisture)
    print("Sensor Reading: ", moisture_reading)
    print("")

if __name__ == "__main__":
    while True:
        read_stats()
        time.sleep(1)
