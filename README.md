# Smart Garden v3

Smart Garden v3 allows users to collectively care for a single house plant. Live moisture, humidity, and temperature data can be used to decide whether the plant should be watered today. Historical trends can be used to track watering patterns and influence future decisions.

## Hardware

The Smart Garden is comprised of the following:

* Raspberry Pi 3B
* Pimoroni Automation pHat Mini
* BMP280 module
* Capacitive Soil Moisture sensor
* 5V DC Submersible Water Pump + Tubing

The Automation Hat allows the Pi to control the water pump via its relay. The analog inputs also allow for capacitive soil moisture readings. 

## Software
The Raspberry Pi runs a Python script which collects sensor data and pushes it to the web app. At the specified time, votes are counted. Majority vote determines whether the water pump is triggered. 

Google Authentication is used to securely prevent duplicate votes. This makes voting fair, safe, and accessible. 

## Setup
TODO!

## History

### Smart Garden v1 (2018-2020)

The original system used the following:

* Raspberry Pi 3B
* Arduino Uno
* 5V DC Water Pump with Silicone Tubing
* 5V Relay
* Conductive Soil Probe

These sub-optimal components caused issues for users over time. The probes would corrode within a few months. The water pump was loud and inconsistent. The two-board setup took up a lot of space. Most notably, voting was limited to daily posts within the r/TakeCareOfOurPlants subreddit, limiting accessibility. In September, 2019, I began working on a new revision.

### Smart Garden v2 (2020-2022):
This newer system was built from the ground up in order to resolve the issues of the original Smart Garden. Here are the parts that were used in the Vote2Grow system:

* Raspberry Pi Zero W
* Pimoroni Automation pHAT Mini
* DHT11 Temperature and Humidity Sensor
* 5V DC Water Pump
* Capacitive Soil Moisture Probe

The biggest change was moving to Google Firebase. Not only would this provide protection in the case that the Raspberry Pi died suddenly before the final vote tally, but it also allowed for votes to be submitted from a variety of sources. The first source of votes, Reddit, remained the same. The only difference was how votes were stored. Instead of a local text file on the Pi, new votes were sent to the database, updating the vote count across all platforms. The second source was a webapp, Vote2Grow. The Arduino was swapped for the Automation pHAT, which made the whole setup more compact. The inconsistent water pump was replaced with a new pump, and the conductive soil probes were swapped for corrosion-free capacitive probes.

### Smart Garden v3 (2022-):
This is the most recent revision of the Smart Garden system. The DHT11 was swapped for a BMP280 module, which adds barometric pressure and altitude readings if desired. The Raspberry Pi Zero W was also swapped for the more powerful Pi 3B. Finally, the web app was redesigned to move away from Google Firebase, which was overkill for this purpose.