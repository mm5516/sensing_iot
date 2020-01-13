#!/usr/bin/env python
import requests
from datetime import datetime
import csv
import tweepy
import schedule
import time
import urllib.request
from urllib.request import urlopen

weather_api_key = "d3c92ad4b84d927d4d1eb09bef058459"
lat = "51.481958"
long = "-0.222531"
rad = "10km"
exc = 'minutely, hourly, daily, alerts, flags'

timenow = datetime.now()

twitter_api_key = 'XE9z1yLludC1xhAJMZxjPt92f'
twitter_api_key_secret = 'JhRa9H9nUxw0OvZxjHkf4MLE5OIrrPml4weiMMm3hKUMzCAiiz'
twitter_access_token = '1216386448057827333-I0LzlGn50y5o9t0fkP5Cov7a1O5Mf3'
twitter_access_token_secret = 'oQC0lQ6JDgZqST3IcopYrvQD42ILbfvBROsxGvTaulUSA'


weather = requests.get('https://api.darksky.net/forecast/%s/%s,%s?exclude=%s?units=si' %(weather_api_key, lat, long, exc)).json()

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")
def get_weather_historical(time, latitude=lat, longitude=long, exclude=exc):
    weather = requests.get('https://api.darksky.net/forecast/%s/%s,%s,%s?exclude=%s?units=si' %(weather_api_key, latitude, longitude, time, exclude)).json()
    current = weather['currently']
    time = current['time']
    temp_f = current['temperature']
    pressure = current['pressure']
    cloudCover = current['cloudCover']
    summary = current['summary']
    temp_c = (temp_f - 32) * 5/9
    date = datetime.fromtimestamp(time)
    date = datetime.utcfromtimestamp(time).strftime('%d.%m.%Y')
    date_time = datetime.utcfromtimestamp(time).strftime('%H:%M:%S')
    print(date, date_time, temp_c, pressure, cloudCover, summary)

def get_weather(latitude=lat, longitude=long, exclude=exc):
    weather = requests.get('https://api.darksky.net/forecast/%s/%s,%s?exclude=%s?units=si' %(weather_api_key, latitude, longitude, exclude)).json()
    current = weather['currently']
    time = current['time']
    temp_f = current['temperature']
    pressure = current['pressure']
    cloudCover = current['cloudCover']
    summary = current['summary']
    temp_c = (temp_f - 32) * 5/9
    date = datetime.fromtimestamp(time)
    date = datetime.utcfromtimestamp(time).strftime('%d.%m.%Y')
    date_time = datetime.utcfromtimestamp(time).strftime('%H:%M:%S')
    return date, date_time, temp_c, pressure, cloudCover, summary

def find_tweets(search_tag, days_ago=-1, minutes_ago_lb=0, minutes_ago_ub=15, latitude=lat, longitude=long, radius=rad):
    tweets = api.search(q="%s" %search_tag, geocode = "%s,%s,%s" %(latitude,longitude,radius), lang="en", count = 100)
    creation_dates = [i.created_at for i in tweets]
    timedelta = [i - timenow for i in creation_dates]
    timedelta_days = [i.days for i in timedelta]
    timedelta_today = [i for i in timedelta_days if i >= days_ago]
    number_today = len(timedelta_today)
    tweets_today = [timedelta[i] for i in range(0,number_today)]
    tweets_today2 = [i.seconds for i in tweets_today]
    tweets_today3 = [ (86400 - i)/60 for i in tweets_today2]
    tweets_recent = [i for i in tweets_today3 if i <= minutes_ago_ub and i >= minutes_ago_lb]
    number_of_newest_tweets = len(tweets_recent)
    return number_of_newest_tweets

def job():
    # positive = find_tweets("positive")
    happy = find_tweets("happy")
    # hopeful = find_tweets("hopeful")
    sad = find_tweets("sad")
    # depressed = find_tweets("depressed")
    # unhappy = find_tweets("unhappy")
    twitter_data = [happy, sad]
    weather_data = get_weather()
    print('hello')
    fieldnames = ['date', 'time','temperature','pressure','cloud cover','summary']
    table = csv.writer(open('/Users/melisamukovic/Desktop/siot_weather/weather_twitter_data.csv', 'a'), lineterminator='\n')
    table.writerow([weather_data[0], weather_data[1], weather_data[2], weather_data[3], weather_data[4], weather_data[5], twitter_data[0], twitter_data[1]])
    urllib.request.urlopen("https://api.thingspeak.com/update?api_key=73KO6AYSP1Q6CIGW&field1=0"+str(weather_data[2]))
    time.sleep(20)
    urllib.request.urlopen("https://api.thingspeak.com/update?api_key=73KO6AYSP1Q6CIGW&field2=0"+str(weather_data[3]))
    time.sleep(20)
    urllib.request.urlopen("https://api.thingspeak.com/update?api_key=73KO6AYSP1Q6CIGW&field3=0"+str(twitter_data[0]))
    time.sleep(20)
    urllib.request.urlopen("https://api.thingspeak.com/update?api_key=73KO6AYSP1Q6CIGW&field4=0"+str(twitter_data[1]))

schedule.every(14).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
