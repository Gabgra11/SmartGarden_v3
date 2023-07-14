import db

def read_and_update_stats():
    # TODO: Get sensor readings:
    moisture, humidity, temperature = None, None, None
    db.add_data_reading(moisture, humidity, temperature)


if __name__ == "__main__":
    read_and_update_stats()