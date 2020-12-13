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

weather_data_ref.push({
    'temperature': 3.2,
    'humidity': 20,
    'pressure': 10,
    'windSpeed': 3.5,
    'windDirectionDegrees': 90,
    'windGust': 2.4,
    'cloudCoverPercentage': 54,
    'rainVolumeLastHour': 0,
    'perceivedTemperature': 2.6,
    'description': 'Cloudy',
    'time': '14:14:45'

})

running_data_ref.push({
'title': 'Lunch Run',
'distance': 7844.3,
'moving_time': 2851,
'total_elevation_gain': 78.0,
'type': 'Run',
'start_date_local': '2020-12-06T11:25:10',
'run_date': run_date,
'start_time': run_start_time,
'end_time': run_end_time,
'start_latlng': [53.361662, -6.25992], 
'end_latlng': [53.362181, -6.260731], 
'summary_polyline': 'keudInsee@Kj@a@xAw@hGw@|Eq@vF_AdG_@nBw@tG_@nC]pBe@zESpAs@lDInAGPIJy@CIGM@{@Aw@Mc@O_@WuAs@}DeB{DyBc@Sa@W_Aa@mAu@s@_@c@]_Ak@g@k@[o@U_@]a@m@cAsAgBuA{BMS]IGGOQWg@e@e@QK_@G_BIy@Ku@MwAKQGEGWIy@]o@QcB[eA[oB_As@Bq@Rq@Fg@LU@y@Ns@H_ARq@He@Gs@XOLq@HoAd@i@JqAZUBgBSyA?g@C_@Em@UGKBmAPo@l@cB`@aBRmAFmBGc@Ce@[_@Sa@OQIBKP[L{A@i@Q]G]Ka@KS[KKCs@@e@Ia@Jq@CKDcAHYFEH?NDl@@h@AXJh@LJABE@a@Bs@Au@O_@Sw@{@_CQu@MQSIOHGHcAhBQTIDM?kBOm@@[GMIO?GBMPOnAHzDKdBFx@KnCDzAAz@FhEBr@AhA@bANb@v@Vp@DjANV?jCf@x@AtABXLRRJFf@Ll@Hp@A`@Dt@Cb@DPHdA@rBk@v@QjAa@DINqA?c@h@eF@e@f@qDR{@NoBB}A|AkLFq@AQPoB?_@Le@?KNe@EUHaBf@gENmBJw@By@Fu@\\yARuALiAJ_@@q@DQDw@XqBVmAJ}@Py@LELUPBJHJ@f@XRPp@`@x@v@d@\\VHf@LZLn@`@vB|@p@PXNXXdAr@d@j@XJb@Tb@h@J@T?NDLNJD\\XRH\\VNBNLp@Rn@ZTRTLPNXNn@Rz@d@d@PfAx@VJdBT^LRBh@XPFPNn@C^K\\ODJl@\\\\@NJj@PfAz@zAn@HFLPPHDHhAz@j@Rv@j@^^`An@d@h@N\\LJJT?LBHLALN|@h@VKDBb@r@LJXN^Zb@l@p@h@NV?Hw@pE',
'average_speed': 2.751,
'max_speed': 4.6,
'average_cadence': 78,
'average_heartrate': 171.0,
'max_heartrate': 189.0
})

while True:
    #print(firstApiArr)
    #print(runningApiCounter)
    #print(weatherDataCounter)
    if weatherDataCounter == 10:
        weather_data_ref.push({
        'temperature': 3.2,
        'humidity': 20,
        'pressure': 10,
        'windSpeed': 3.5,
        'windDirectionDegrees': 90,
        'windGust': 2.4,
        'cloudCoverPercentage': 54,
        'rainVolumeLastHour': 0,
        'perceivedTemperature': 2.6,
        'description': 'Cloudy',
        'time': '14:14:45'
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
        print(len(firstApiArr) == len(secondApiArr))
        runningApiCounter = 0
        weatherDataCounter = 0

    
    #print(firstApiCallRunsArray)

    runningApiCounter = runningApiCounter + 1
    weatherDataCounter = weatherDataCounter + 1

    time.sleep(6)






running_data_ref.push({
'title': 'Lunch Run',
'distance': 7844.3,
'moving_time': 2851,
'total_elevation_gain': 78.0,
'type': 'Run',
'start_date_local': '2020-12-06T11:25:10',
'run_date': run_date,
'start_time': run_start_time,
'end_time': run_end_time,
'start_latlng': [53.361662, -6.25992], 
'end_latlng': [53.362181, -6.260731], 
'summary_polyline': 'keudInsee@Kj@a@xAw@hGw@|Eq@vF_AdG_@nBw@tG_@nC]pBe@zESpAs@lDInAGPIJy@CIGM@{@Aw@Mc@O_@WuAs@}DeB{DyBc@Sa@W_Aa@mAu@s@_@c@]_Ak@g@k@[o@U_@]a@m@cAsAgBuA{BMS]IGGOQWg@e@e@QK_@G_BIy@Ku@MwAKQGEGWIy@]o@QcB[eA[oB_As@Bq@Rq@Fg@LU@y@Ns@H_ARq@He@Gs@XOLq@HoAd@i@JqAZUBgBSyA?g@C_@Em@UGKBmAPo@l@cB`@aBRmAFmBGc@Ce@[_@Sa@OQIBKP[L{A@i@Q]G]Ka@KS[KKCs@@e@Ia@Jq@CKDcAHYFEH?NDl@@h@AXJh@LJABE@a@Bs@Au@O_@Sw@{@_CQu@MQSIOHGHcAhBQTIDM?kBOm@@[GMIO?GBMPOnAHzDKdBFx@KnCDzAAz@FhEBr@AhA@bANb@v@Vp@DjANV?jCf@x@AtABXLRRJFf@Ll@Hp@A`@Dt@Cb@DPHdA@rBk@v@QjAa@DINqA?c@h@eF@e@f@qDR{@NoBB}A|AkLFq@AQPoB?_@Le@?KNe@EUHaBf@gENmBJw@By@Fu@\\yARuALiAJ_@@q@DQDw@XqBVmAJ}@Py@LELUPBJHJ@f@XRPp@`@x@v@d@\\VHf@LZLn@`@vB|@p@PXNXXdAr@d@j@XJb@Tb@h@J@T?NDLNJD\\XRH\\VNBNLp@Rn@ZTRTLPNXNn@Rz@d@d@PfAx@VJdBT^LRBh@XPFPNn@C^K\\ODJl@\\\\@NJj@PfAz@zAn@HFLPPHDHhAz@j@Rv@j@^^`An@d@h@N\\LJJT?LBHLALN|@h@VKDBb@r@LJXN^Zb@l@p@h@NV?Hw@pE',
'average_speed': 2.751,
'max_speed': 4.6,
'average_cadence': 78,
'average_heartrate': 171.0,
'max_heartrate': 189.0
})







sortedRunsArray = sorted(runsArray, key=lambda x: datetime.strptime(x['start_date_local'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

print(sortedRunsArray)


newNumberOfRunsCount = len(runsArray)


newRunDistance = runsArray[0]["distance"]
newRunMovingTime = runsArray[0]["elapsed_time"]
newRunElevationGain = runsArray[0]["total_elevation_gain"]
#Need to format this
newRunStartDate = runsArray[0]["start_date_local"]
newRunAverageHeartRate = runsArray[0]["average_heartrate"]
newRunMaxHeartRate = runsArray[0]["max_heartrate"]
#Possibly push start and end latitude and longitude if I can figure out how to display this via Google Map (NICE TO HAVE)

#Figure out how strava pushes speed back - might be miles per hour from look of API response





print(newRunDistance)


if newNumberOfRunsCount - oldNumberOfRunsCount == 1:
    #push to Firebase
    a = b


#Setting length of array before nextAPIcheck
oldNumberOfRunsCount = newNumberOfRunsCount

#openWeatherResponse = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + latitude + "&lon=" + longitude + "&units=metric&exclude=hourly,minutely,daily&appid=" + apiKey)

#openWeatherJsonResponse = openWeatherResponse.json()
#apiResponseTemp = openWeatherJsonResponse["current"]["temp"]
#apiResponsePerceivedTemp = openWeatherJsonResponse["current"]["feels_like"]
#apiResponsePressure = openWeatherJsonResponse["current"]["pressure"]
#apiResponseWindSpeed = openWeatherJsonResponse["current"]["wind_speed"]
#apiResponseWindDegree = openWeatherJsonResponse["current"]["wind_deg"]
#apiResponseWindGust = openWeatherJsonResponse["current"]["wind_gust"]
#apiResponseWeatherDescription = openWeatherJsonResponse["current"]["weather"]["main"]



#sense = SenseHat()

#sensehatTemp = round(sense.get_temperature(), 2)
#sensehatPressure = round(sense.get_pressure(), 2)
#sensehatHumidity = round(sense.get_humidity(), 2)
