# [🪴 www.Vote2Grow.com 🪴](https://www.Vote2Grow.com)

# Smart Garden v3

Smart Garden v3 allows users to collectively care for a single house plant. Live moisture, humidity, and temperature data can be used to decide whether the plant should be watered today. Historical trends can be used to track watering patterns and influence future decisions.


## Hardware

Smart Garden uses the following hardware:

* Raspberry Pi Zero W + PSU
* Pimoroni Automation HAT Mini
* BME280 module
* Capacitive Soil Moisture sensor
* USB Web Cam + Micro USB to USB Adapter
* 5V DC Submersible Water Pump + Tubing + PSU

The Automation Hat allows the Pi to control the water pump via its relay. The analog inputs also allow for capacitive soil moisture readings.

1. Wire up the sensors/pump as follows:
    - Capacitive Sensor Output to A1 on the Pi HAT
    - Capacitive Sensor 5v and Ground to 5v and Ground on the Pi Hat
    - Water Pump PSU Ground to Ground on the Pi HAT
    - Water Pump PSU 5v to COM on the Pi HAT Relay
    - Water Pump 5v Input to NO on the Pi HAT Relay
    - BME280 to I2C on the Pi HAT
2. Connect the Pi Hat to the Raspberry Pi Zero W
3. Plug the USB web cam into the micro USB port using a micro USB to USB adapter.
4. Plug the Pi PSI and the Water Pump PSU into wall power.


## Software

The Raspberry Pi runs a Python script which collects sensor data and pushes it to the web app's database. Another script is run at midnight to count the votes. Majority vote determines whether the water pump is triggered. 

Google Sign In from Google Cloud Platform is used to securely prevent duplicate votes. This makes voting fair, safe, and accessible.

A PostgreSQL database is used for storing votes, sensor data, and other relevant data. An easy way to host the web app and PostgreSQL server is AWS Elastic Beanstalk with AWS RDS.

### 1. Setting up the environment
___
Clone the repository onto the Raspberry Pi and set the following environment variables:

```
client_id=[Google Cloud Platform Client ID]
client_secret="[Google Cloud Platform Client Secret (with quotes)]"
db_url=[Database Connection URL]
login_uri=/login
IMGUR_CLIENT_ID=[Imgur API Client ID (If using webcam)]
IMGUR_CLIENT_SECRET=[Imgur API Client Secret (If using webcam)]
```

Install the necessary requirements with:

```
pip install -r requirements.txt
```

Configure the crontab according to this example:

```
client_id=[Google Cloud Platform Client ID]
client_secret="[Google Cloud Platform Client Secret (with quotes)]"
db_url=[Database Connection URL]
login_uri=/login
IMGUR_CLIENT_ID=[Imgur API Client ID (If using webcam)]
IMGUR_CLIENT_SECRET=[Imgur API Client Secret (If using webcam)]

0 0 * * * python ~/SmartGarden_v3/water.py
0 13 * * * python ~/SmartGarden_v3/update_live_photo.py
*/15 * * * * python ~/SmartGarden_v3/read_sensors.py
```

The example above counts votes and waters at midnight, updates the live photo at 1 pm, and reads the sensors every 15 minutes.
<br/><br/>
### 2. Setting up the SQL database
___
From the root directory, navigate to /db/:

```
cd db
```

and run:
```
python init_db.py
```

This will create the necessary tables from the schema specified in ```schema.sql```. This script can be run again at any time to clear **all** entries in the database.
<br/><br/>
### 3. Testing the web app
___
To test the web app locally, ensure you are in the root directory and run:

```
flask --debug --app=application.py run
```

To add posts to the 'News' tab, run the following command locally:


```
python news_app.py
```

then go to [http://localhost:5001](http://localhost:5001) in your web browser, and submit the post.


## History

### Smart Garden v1 (2018-2020)

The original system used the following:

* Raspberry Pi 3B
* Arduino Uno
* 5V DC Water Pump with Silicone Tubing
* 5V Relay
* Conductive Soil Probe

These sub-optimal components caused issues for users over time. The probes would corrode within a few months. The water pump was loud and inconsistent. The two-board setup took up a lot of space. Most notably, voting was limited to daily posts within the r/TakeCareOfOurPlants subreddit, limiting accessibility. In September, 2019, I began working on a new revision.

### Smart Garden v2 (2020-2022)
This newer system was built from the ground up in order to resolve the issues of the original Smart Garden. Here are the parts that were used in the Vote2Grow system:

* Raspberry Pi Zero W
* Pimoroni Automation pHAT Mini
* DHT11 Temperature and Humidity Sensor
* 5V DC Water Pump
* Capacitive Soil Moisture Probe

The biggest change was moving to Google Firebase. Not only would this provide protection in the case that the Raspberry Pi died suddenly before the final vote tally, but it also allowed for votes to be submitted from a variety of sources. The first source of votes, Reddit, remained the same. The only difference was how votes were stored. Instead of a local text file on the Pi, new votes were sent to the database, updating the vote count across all platforms. The second source was a webapp, Vote2Grow. The Arduino was swapped for the Automation pHAT, which made the whole setup more compact. The inconsistent water pump was replaced with a new pump, and the conductive soil probes were swapped for corrosion-free capacitive probes.

### Smart Garden v3 (2022-)
This is the most recent revision of the Smart Garden system. The entire web app was rewritten for optimized performance and improved user experience. Smart Garden v3 has been moved from Google Firebase to Amazon Web Services. The hardware remains the same, but everything has been refreshed under the hood.
