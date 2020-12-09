import json
import time
import requests
import config
from datetime import datetime
#from sense_hat import SenseHat

latitude = '53.3634'
longitude = '6.2579'
apiKey = config.openWeatherApiKey

stravaClientId = config.stravaClientId
stravaClientSecret = config.stravaClientSecret


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

runsArray = []

for x in range(len(r)):
    if r[x]["type"] == 'Run':
        runsArray.append(r[x])
    #print(r[x]["name"])
    #print(x)

#print(r)

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