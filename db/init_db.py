import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()

# TODO: Remove this! For testing purposes only:
connection.execute('INSERT INTO data (timestamp, moisture, humidity, temperature) VALUES \
    (1675296001, 85.2, 29.9, 70.4), \
    (1675382401, 66.4, 30.1, 71.0), \
    (1675468801, 45.2, 30.2, 70.9), \
    (1675555201, 88.8, 29.8, 69.9), \
    (1675641601, 67.9, 29.8, 70.2), \
    (1675728001, 51.3, 30.1, 71.0), \
    (1675814401, 44.2, 30.0, 71.2);')
connection.commit()
# TODO: Remove this! For testing purposes only ^

connection.close()