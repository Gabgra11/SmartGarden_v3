from scripts import db
import automationhat
import smbus2
import bme280

def read_and_update_stats():
    # TODO: Get sensor readings:
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    moisture = automationhat.analog.one.read()
    # TODO: Map analog reading to moisture %
    temperature = (data.temperature * (9/5)) + 32
    humidity = data.humidity
    print("Temperature (F): ", temperature)
    print("Moisture: ", moisture)
    print("Humidity: ", humidity)
    db.add_data_reading(moisture, humidity, temperature)


if __name__ == "__main__":
    read_and_update_stats()
