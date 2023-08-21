from scripts import db
import automationhat
import smbus2
import bme280

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

def read_and_update_stats():
    # TODO: Get sensor readings:
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    moisture_reading = automationhat.analog.one.read()
    moisture = analog_reading_to_percent(moisture_reading)
    temperature = (data.temperature * (9/5)) + 32
    humidity = data.humidity

    moisture = truncate(moisture, 1)
    temperature = truncate(temperature, 1)
    humidity = truncate(humidity, 1)
    print("Temperature (F): ", temperature)
    print("Moisture: ", moisture)
    print("Humidity: ", humidity)
    db.add_data_reading(moisture, humidity, temperature)


if __name__ == "__main__":
    read_and_update_stats()
