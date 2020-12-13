import json
import time
import requests
import config
from datetime import datetime, date, timedelta
import threading
#from sense_hat import SenseHat

import firebase_admin
from firebase_admin import credentials, firestore, storage, db

runningApiCounter = 0
weatherDataCounter = 0

latitude = '53.3634'
longitude = '-6.2579'


cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://weather-running-performance-default-rtdb.firebaseio.com/'
})


date = '2020-12-06T11:25:10'
endTimeStr = date[(date.index('T') + 1): ]
endTimeObject = datetime.strptime(endTimeStr, '%H:%M:%S')
moving_time = 2851

def convert(n): 
    #return str(endTimeObject + timedelta(seconds = n)) 
    test = str(endTimeObject + timedelta(seconds = n))
    testRef = test[11:]
    return testRef
    #return datetime.strptime(testRef, '%H:%M:%S')
    #return test.minutes



run_end_time = convert(moving_time) 

start_date_local = '2020-12-06T11:25:10'

def obtainRunDate(unformattedDateString):
    return unformattedDateString[ :(unformattedDateString.index('T'))]


run_date = obtainRunDate(start_date_local)

def obtainRunStartTime(unformattedDateString):
    return unformattedDateString[(unformattedDateString.index('T') + 1) :]

run_start_time = obtainRunStartTime(start_date_local)

#firstApiCallRunsArray = []
firstApiCallRunsArray = threading.Event()
firstApiArr = None

secondApiCallRunsArray = threading.Event()
secondApiArr = None

def populatingFirstApiCallRunArray (numberOfRuns, r):
    testArr = []
    #for x in range(len(numberOfRuns)):
    for x in range(numberOfRuns):
        if r[x]["type"] == 'Run':
            #firstApiCallRunsArray.append(r[x])
            testArr.append(r[x])
    
    global firstApiArr
    #print(testArr)
    firstApiArr = testArr
    #print(firstApiArr)
    firstApiCallRunsArray.set()
    return testArr
    #time.sleep(5)


def populatingSecondApiCallRunArray (numberOfRuns, r):
    testArr = []
    #for x in range(len(numberOfRuns)):
    for x in range(numberOfRuns):
        if r[x]["type"] == 'Run':
            #firstApiCallRunsArray.append(r[x])
            testArr.append(r[x])
    
    global secondApiArr
    #print(testArr)
    secondApiArr = testArr
    #print(firstApiArr)
    secondApiCallRunsArray.set()
    return testArr
    #time.sleep(5)

#Firebase good to go
ref = db.reference('/')
weather_data_ref = ref.child('weatherData')
running_data_ref = ref.child('runningData')



while True:
    #print(firstApiArr)
    #print(runningApiCounter)
    #print(weatherDataCounter)
    print(weatherDataCounter)
    if weatherDataCounter == 5:

        openWeatherResponse = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + latitude + "&lon=" + longitude + "&units=metric&exclude=hourly,minutely,daily&appid=" + config.openWeatherApiKey)

        openWeatherJsonResponse = openWeatherResponse.json()
        apiResponseTemp = openWeatherJsonResponse["current"]["temp"]
        apiResponsePerceivedTemp = openWeatherJsonResponse["current"]["feels_like"]
        apiResponsePressure = openWeatherJsonResponse["current"]["pressure"]
        apiResponseWindSpeed = openWeatherJsonResponse["current"]["wind_speed"]
        apiResponseWindDegree = openWeatherJsonResponse["current"]["wind_deg"]
        apiResponseWindGust = openWeatherJsonResponse["current"]["wind_gust"]
        apiResponseCloudCover = openWeatherJsonResponse["current"]["clouds"]

        if "rain" not in openWeatherJsonResponse:
            apiResponseRainLastHour = 0
        else:
            apiResponseRainLastHour = openWeatherJsonResponse["current"]["rain"]["1h"]


        apiResponseWeatherDescription = openWeatherJsonResponse["current"]["weather"][0]["main"]

        now = datetime.now()
        currentTime = now.strftime("%H:%M:%S")



        #sense = SenseHat()

        #sensehatTemp = round(sense.get_temperature(), 2)
        #sensehatPressure = round(sense.get_pressure(), 2)
        #sensehatHumidity = round(sense.get_humidity(), 2)
        #MAY PUSH TEMP FROM EITHER API RESPONSE OR SENSEHAT

        weather_data_ref.push({
        'temperature': apiResponseTemp,
        'humidity': 20,
        'pressure': apiResponsePressure,
        'windSpeed': apiResponseWindSpeed,
        'windDirectionDegrees': apiResponseWindDegree,
        'windGust': apiResponseWindGust,
        'cloudCoverPercentage': apiResponseCloudCover,
        'rainVolumeLastHour': apiResponseRainLastHour,
        'perceivedTemperature': apiResponsePerceivedTemp,
        'description': apiResponseWeatherDescription,
        'time': currentTime
        })
        weatherDataCounter = 0
#I think 300 will be good for production
    if runningApiCounter == 5:
        print("Starting anyway")
        
        
        ## Get the tokens from file to connect to Strava
        with open('strava_tokens.json') as json_file:
           
            strava_tokens = json.load(json_file)
## If access_token has expired then use the refresh_token to get the new access_token
        if strava_tokens['expires_at'] < time.time():
           
    # Make Strava auth API call with your 
# client_code, client_secret and code
            response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': stravaClientId,
                            'client_secret': stravaClientSecret,
                             'grant_type': 'refresh_token',
                              'refresh_token': strava_tokens['refresh_token']
                            }
                )
#Save response as json in new variable
            new_strava_tokens = response.json()

    # Save new tokens to file
            with open('strava_tokens.json', 'w') as outfile:
               json.dump(new_strava_tokens, outfile)

        #Use new Strava tokens from now
               strava_tokens = new_strava_tokens


    #Loop through all activities
        page = 1
        url = "https://www.strava.com/api/v3/activities"
        access_token = strava_tokens['access_token']


 # get page of activities from Strava
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()


            #thread = threading.Thread(target=populatingFirstApiCallRunArray, args=(len(r), r))
            #thread.start()

           
        thread = threading.Thread(target=populatingFirstApiCallRunArray, args=(len(r), r))
        thread.start()
        #firstApiArr = firstApiCallRunsArray.wait()
        firstApiCallRunsArray.wait()
        print(len(firstApiArr))
        
        
        

        #runningApiCounter = 0
          #for x in range(len(r)):
             #if r[x]["type"] == 'Run':
                #firstApiCallRunsArray.append(r[x])
    
    
    
    #print(r[x]["name"])
    #print(x)
          #print(len(firstApiCallRunsArray))
          #print(firstApiCallRunsArray)

#print(r)

    if runningApiCounter == 8:
        print("Starting for second time")
        
        
        ## Get the tokens from file to connect to Strava
        with open('strava_tokens.json') as json_file:
           
            strava_tokens = json.load(json_file)
## If access_token has expired then use the refresh_token to get the new access_token
        if strava_tokens['expires_at'] < time.time():
           
    # Make Strava auth API call with your 
# client_code, client_secret and code
            response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': stravaClientId,
                            'client_secret': stravaClientSecret,
                             'grant_type': 'refresh_token',
                              'refresh_token': strava_tokens['refresh_token']
                            }
                )
#Save response as json in new variable
            new_strava_tokens = response.json()

    # Save new tokens to file
            with open('strava_tokens.json', 'w') as outfile:
               json.dump(new_strava_tokens, outfile)

        #Use new Strava tokens from now
               strava_tokens = new_strava_tokens


    #Loop through all activities
        page = 1
        url = "https://www.strava.com/api/v3/activities"
        access_token = strava_tokens['access_token']


 # get page of activities from Strava
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()


            #thread = threading.Thread(target=populatingFirstApiCallRunArray, args=(len(r), r))
            #thread.start()

           
        thread = threading.Thread(target=populatingSecondApiCallRunArray, args=(len(r), r))
        thread.start()
        #firstApiArr = firstApiCallRunsArray.wait()
        secondApiCallRunsArray.wait()
        print(len(firstApiArr))
        

        #Checking to see if new activity is present. If so it will need to be pushed to Firebase
        if len(firstApiArr) != len(secondApiArr):
            sortedRunsArray = sorted(secondApiArr, key=lambda x: datetime.strptime(x['start_date_local'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
            #newRunDistance = runsArray[0]["distance"]
            newRunTitle = sortedRunsArray[0]["name"]
            newRunDistance = sortedRunsArray[0]["distance"]
            newRunMovingTime = sortedRunsArray[0]["elapsed_time"]
            newRunElevationGain = sortedRunsArray[0]["total_elevation_gain"]
            newRunType = sortedRunsArray[0]["type"]
            #Need to format this
            newRunStartDateLocal = sortedRunsArray[0]["start_date_local"]
            newRunDate = obtainRunDate(newRunStartDateLocal)
            newRunStartTime = obtainRunStartTime(newRunStartDateLocal)
            newRunEndTime = convert(newRunMovingTime)
            newRunStartLatitudeLongitude = sortedRunsArray[0]["start_latlng"]
            newRunEndLatitudeLongitude = sortedRunsArray[0]["end_latlng"]
            newRunSummaryPolyline = sortedRunsArray[0]["map"]["summary_polyline"]
            newRunAverageSpeed = sortedRunsArray[0]["average_speed"]
            newRunMaxSpeed = sortedRunsArray[0]["max_speed"]
            newRunAverageCadence = sortedRunsArray[0]["average_cadence"]
            newRunAverageHeartRate = sortedRunsArray[0]["average_heartrate"]
            newRunMaxHeartRate = sortedRunsArray[0]["max_heartrate"]

            running_data_ref.push({
            'title': newRunTitle,
            'distance': newRunDistance,
            'moving_time': newRunMovingTime,
            'total_elevation_gain': newRunElevationGain,
            'type': newRunType,
            'start_date_local': newRunStartDateLocal,
            'run_date': newRunDate,
            'start_time': newRunStartTime,
            'end_time': newRunEndTime,
            'start_latlng': newRunStartLatitudeLongitude, 
            'end_latlng': newRunEndLatitudeLongitude, 
            'summary_polyline': newRunSummaryPolyline,
            'average_speed': newRunAverageSpeed,
            'max_speed': newRunMaxSpeed,
            'average_cadence': newRunAverageCadence,
            'average_heartrate': newRunAverageHeartRate,
            'max_heartrate': newRunMaxHeartRate
            })






        runningApiCounter = 0
        weatherDataCounter = 0

    
    #print(firstApiCallRunsArray)

    #Commenting out to save on Strava API calls
    #runningApiCounter = runningApiCounter + 1
    weatherDataCounter = weatherDataCounter + 1



    time.sleep(3)