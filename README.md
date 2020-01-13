# DE4 Sensing and Internet of Things
### Atmospheric Wellbeing Platform

This repository is the documentation of the creation of the Atmospheric Wellbeing Platform as part of the DE4 Sensing and IoT module. The project uses Dark Sky API and Twitter API via Tweepy to create a platform which shares information on the connections between weather conditions and mental wellbeing.

[The AWP platform can be accessed here](https://mukovicmelisa.wixsite.com/mysite)

The files included in this repository are: `weather.py` which contains the main sensing code, appending gathered data to `weather_twitter_data.csv`, which is later accessed by the Jupyter notebook `weather_data.ipynb` for data manipulation, and analysis. The graphs created in this notebook are later used on the digital platform linked above.

This project uses the following python libraries:
- requests
- tweepy
- datetime
- csv
- schedule
- urllib.request
- plotly
- numpy
- pandas
- matplotlib
