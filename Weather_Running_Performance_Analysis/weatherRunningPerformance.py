# Importing config file that contains all API keys and other sensitive data
import config

# json is used to parse api responses
import json
import time
# Requests module used to make api calls to 3rd party services
import requests
from datetime import datetime, date, timedelta
import threading
# Twilio is the 3rd party service used to send SMS messages (on addition of new running activity)
from twilio.rest import Client
# SenseHat is used to obtain weather data from the hat attached to the Raspberry Pi
from sense_hat import SenseHat
# Firebase_admin is used to establish a connection between the program and the Firebase Realtime Database
import firebase_admin
from firebase_admin import credentials, firestore, storage, db

account_sid = config.twilio_account_sid
auth_token = config.twilio_auth_token

# Initiating Twilio client
client = Client(account_sid, auth_token)

# Declaring SenseHat
sense = SenseHat()
sense.clear()

# Setting latitude and longitude for Drumcondra, Dublin
latitude = '53.3634'
longitude = '-6.2579'
apiKey = config.openWeatherApiKey

# Initialising counter variables for the API call intervals
runningApiCounter = 0
weatherDataCounter = 0

stravaClientId = 57806
stravaClientSecret = config.stravaClientSecret

cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://weather-running-performance-default-rtdb.firebaseio.com/'
})

# Declaring references for Firebase Realtime Database
ref = db.reference('/')
weather_data_ref = ref.child('weatherData')
running_data_ref = ref.child('runningData')

date = '2020-12-06T11:25:10'
endTimeStr = date[(date.index('T') + 1): ]
endTimeObject = datetime.strptime(endTimeStr, '%H:%M:%S')
moving_time = 2851

# Declaring convert function to strip time from date and time string
def convert(n): 
    string = str(endTimeObject + timedelta(seconds = n))
    timeString = string[11:]
    return timeString
    



run_end_time = convert(moving_time) 

start_date_local = '2020-12-06T11:25:10'

# Declaring function to obtain run date from string that contains both date and time
def obtainRunDate(unformattedDateString):
    return unformattedDateString[ :(unformattedDateString.index('T'))]


run_date = obtainRunDate(start_date_local)

# Declaring function to obtain run start time from string that contains both date and time
def obtainRunStartTime(unformattedDateString):
    return unformattedDateString[(unformattedDateString.index('T') + 1) : (unformattedDateString.index('Z'))]



# Declaring variable that will be set to result of threading event
firstApiCallRunsArray = threading.Event()
# Initially setting firstApiArr to None (will be used to store results of first API call to Strava)
firstApiArr = None

# Declaring variable that will be set to result of threading event
secondApiCallRunsArray = threading.Event()
# Initially setting secondApiArr to None (will be used to store results of second API call to Strava)
secondApiArr = None

# Declaring function to loop through first API response from Strava and only filter activities that are equal to 'Run'. The firstApiCallRunsArray thread is then set
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


# Declaring function to loop through second API response from Strava and only filter activities that are equal to 'Run'. The secondApiCallRunsArray thread is then  set
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
    



# To keep the program running indefinitely, a while True loop is initiated
while True:
    #print(firstApiArr)
    print(runningApiCounter)
    #print(weatherDataCounter)
    #print(weatherDataCounter)

    # If the weatherDataCounter variable equals 12, an API call is made to OpenWeatherMap and a weather data reading is also obtained from the SenseHat
    if weatherDataCounter == 12:
        # The API is passed the latitude and longitude variables (that were set at the beginning of the program)
        openWeatherResponse = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + latitude + "&lon=" + longitude + "&units=metric&exclude=hourly,minutely,daily&appid=" + apiKey)

        # The response is serialised using JSON
        openWeatherJsonResponse = openWeatherResponse.json()

        # A number of variables are set according to the API response mapping
        apiResponseTemp = openWeatherJsonResponse["current"]["temp"]
        apiResponsePerceivedTemp = openWeatherJsonResponse["current"]["feels_like"]
        apiResponsePressure = openWeatherJsonResponse["current"]["pressure"]
        apiResponseWindSpeed = openWeatherJsonResponse["current"]["wind_speed"]
        apiResponseWindDegree = openWeatherJsonResponse["current"]["wind_deg"]

        # Wind gust is not always sent back (if there is no wind gust currently): therefore some simple error validation is in place to ensure that this defaults to 0 if it is not present in the API response
        if "wind_gust" not in openWeatherJsonResponse:
            apiResponseWindGust = 0
        else:
            apiResponseWindGust = openWeatherJsonResponse["current"]["wind_gust"]
        
        apiResponseCloudCover = openWeatherJsonResponse["current"]["clouds"]

        # A value for rain is not always sent back (if there is no rain currently): therefore some simple error validation is in place to ensure that this defaults to 0 if it is not present in the API response
        if "rain" not in openWeatherJsonResponse:
            apiResponseRainLastHour = 0
        else:
            apiResponseRainLastHour = openWeatherJsonResponse["current"]["rain"]["1h"]


        apiResponseWeatherDescription = openWeatherJsonResponse["current"]["weather"][0]["main"]

        # Setting the timestamp to the current time
        now = datetime.now()

        # Stripping the hour, minute and second values from the datetime value
        currentTime = now.strftime("%H:%M:%S")



       
        # Values from sensehat are rounded to 2 decimal places
        sensehatTemp = round(sense.get_temperature_from_pressure(), 2)
        sensehatPressure = round(sense.get_pressure(), 2)
        sensehatHumidity = round(sense.get_humidity(), 2)
        

        # Values from both the OpenWeatherMap API response and the Sensehat are pushed to Firebase (as well as the timestamp)
        weather_data_ref.push({
        'outdoor_temperature': apiResponseTemp,
        'indoor_temperature': sensehatTemp,
        'humidity': sensehatHumidity,
        'pressure': sensehatPressure,
        'windSpeed': apiResponseWindSpeed,
        'windDirectionDegrees': apiResponseWindDegree,
        'windGust': apiResponseWindGust,
        'cloudCoverPercentage': apiResponseCloudCover,
        'rainVolumeLastHour': apiResponseRainLastHour,
        'perceivedTemperature': apiResponsePerceivedTemp,
        'description': apiResponseWeatherDescription,
        'time': currentTime
        })

        # weatherDataCounter is reset to 0
        weatherDataCounter = 0

        # Sense hat is cleared
        sense.clear()
#I think 300 will be good for production

    # If the value of runningApiCounter is equal to 1, call the Strava API to see the current number of run activites that are recorded
    if runningApiCounter == 1:
        print("Starting anyway")
        
        
        # Strava API access tokens are obtained
        with open('strava_tokens.json') as json_file:
           
            strava_tokens = json.load(json_file)
        # If access_token has expired then use the refresh_token to get the new access_token
        if strava_tokens['expires_at'] < time.time():
           
            # Make authorisation API call to Strava
            response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': stravaClientId,
                            'client_secret': stravaClientSecret,
                             'grant_type': 'refresh_token',
                              'refresh_token': strava_tokens['refresh_token']
                            }
                )
            # Save response as json in new variable
            new_strava_tokens = response.json()

            # Save new tokens to file
            with open('strava_tokens.json', 'w') as outfile:
               json.dump(new_strava_tokens, outfile)

            # Use new Strava tokens from now
               strava_tokens = new_strava_tokens


        # Setting values that will be passed to API call for Strava
        page = 1
        url = "https://www.strava.com/api/v3/activities"
        access_token = strava_tokens['access_token']


        # Activity data is obtained from Strava (via API call)
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()

        # Setting thread for populatingFirstApiCallRunArray function (as it can take a few seconds for the response to be parsed and looped)   
        thread = threading.Thread(target=populatingFirstApiCallRunArray, args=(len(r), r))

        # Starting the thread
        thread.start()
        
        # Waiting for the firstApiCallRunsArray variable to be populated by the initiated thread before progressing
        firstApiCallRunsArray.wait()
        print(len(firstApiArr))
        
        
        

    # If the value of runningApiCounter is equal to 2, call the Strava API again to check if a new run activity has been added in the meantime
    if runningApiCounter == 2:
        print("Starting for second time")
        
        
        # API tokens are obtained from file
        with open('strava_tokens.json') as json_file:
           
            strava_tokens = json.load(json_file)
        # If access_token has expired then the refresh_token is used to get the new access_token
        if strava_tokens['expires_at'] < time.time():
           
            # Authorisation API call is made to Strava
            response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': stravaClientId,
                            'client_secret': stravaClientSecret,
                             'grant_type': 'refresh_token',
                              'refresh_token': strava_tokens['refresh_token']
                            }
                )
            # Response is saved as json in new variable
            new_strava_tokens = response.json()

            # New tokens are saved to file
            with open('strava_tokens.json', 'w') as outfile:
               json.dump(new_strava_tokens, outfile)

            # New Strava tokens will be used from now on (until they expire again)
               strava_tokens = new_strava_tokens


        # Setting values that will be passed to API call for Strava
        page = 1
        url = "https://www.strava.com/api/v3/activities"
        access_token = strava_tokens['access_token']


        # Activity data is obtained from Strava (via API call)
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()



        # Setting thread for populatingSecondApiCallRunArray function (as it can take a few seconds for the response to be parsed and looped) 
        thread = threading.Thread(target=populatingSecondApiCallRunArray, args=(len(r), r))

        # Starting the thread
        thread.start()
        
        # Waiting for the secondApiCallRunsArray variable to be populated by the initiated thread before progressing
        secondApiCallRunsArray.wait()
        print(len(firstApiArr))
        

        # Checking to see if new activity is present (by comparing the length of firstApiArr against secondApiArr - both set from Strava API calls). If numbers are not equal a new run activity must have been uploaded to Strava and this needs to be pushed to Firebase
        if len(firstApiArr) != len(secondApiArr):

            # Sorting the secondApiArr by date to ensure that only the new activity that has been added is pushed to Firebase
            sortedRunsArray = sorted(secondApiArr, key=lambda x: datetime.strptime(x['start_date_local'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

            # A number of variables are declared and initialised with the relevant values from the sortedRunsArray (as it has been sorted, the latest activity is at index position 0)
            newRunTitle = sortedRunsArray[0]["name"]
            newRunDistance = sortedRunsArray[0]["distance"]
            newRunMovingTime = sortedRunsArray[0]["elapsed_time"]
            newRunElevationGain = sortedRunsArray[0]["total_elevation_gain"]
            newRunType = sortedRunsArray[0]["type"]
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


            # New running activity data is pushed to Firebase
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

            # Message is sent to my phone informing me that a new activity has been uploaded to Firebase. A link to the Glitch application is included in the text for ease of access
            message = client.messages.create(
                from_='+16193893728',
                body='A new activity has been added to the dashboard. Take a look: https://weather-impact-on-running-performance.glitch.me/',
                to='+353873101875'
            )





        # runningApiCounter is reset to 0
        runningApiCounter = 0
        #weatherDataCounter = 0

    
    #print(firstApiCallRunsArray)

    # runningApiCounter and weatherDataCounter are both incremented by 1 at the end of the program loop
    runningApiCounter = runningApiCounter + 1
    weatherDataCounter = weatherDataCounter + 1


    # The program sleeps for 10 seconds before running again. 10 seconds is used as the interval as the Strava API only allows 150 API calls in a 15 minute period
    time.sleep(10)