from __future__ import division
import paho.mqtt.publish as publish
import picamera
import time
import numpy as np
import requests
import json
import datetime
from gpiozero import LED
from gpiozero import MotionSensor

# Importing config file to obtain access to API keys and other sensitive information required for 3rd party services
import config


# Setting default width and height for image
width = 100
height = 100

# Setting variable for green LED at GPIO Pin 17
green_led = LED(17)
# Setting variable for PIR Motion sensor at GPIO pin 4
pir = MotionSensor(4)
# LED is initially set to off
green_led.off()

# This array is used to store value of PIR motion sensor response each second. If a 1 is present, push to ThingSpeak indicates that motion was detected (free tier only allows a data push every 15 seconds)
arrayOfValues = []

# Setting count interval for api calls
apiSecondCount = 0
motionDetected = 0

# Indefinite loop to keep program running
while True:
   #Increase the count interval by 1
   apiSecondCount+= 1
   # Append the current value of the pir motion sensor to the arrayOfValues Array (0 if no motion, 1 if motion detected)
   arrayOfValues.append(pir.value)

   # Beginning a stream for the PiCamera
   stream = open('image.data', 'w+b')
   # Capturing the image in YUV format
   with picamera.PiCamera() as camera:
      camera.resolution = (width, height)
      camera.start_preview()
      time.sleep(2)
      camera.capture(stream, 'yuv')
      #The stream is rewound so that the data can be read
      stream.seek(0)
      # Image size in the stream (accounting for rounding
      # of the resolution) is calculated
      fwidth = (width + 31) // 32 * 32
      fheight = (height + 15) // 16 * 16
      # The Y (luminance) data from the stream is loaded
      Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
         reshape((fheight, fwidth))
   avgLuminancePerPixelArray = []
   pixelLuminance = 0
   count = 0
   print(len(Y))




   # API call to Mapbox to receive longitude and latitude for current location
   currentLocation = "Drumcondra"
   # apiCallCount is initially set to zero
   apiCallCount = 0
   
   # If statement to check if the value in currentLocation variable has been changed from Drumcondra (or the apiCallCount is 0)
   if (currentLocation.upper() != "DRUMCONDRA" or apiCallCount == 0):
      # If either of those conditions are true, an API call is made to Mapbox to obtain the latitude and longitude for the current location
      mapboxResponse = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/" + currentLocation + ".json?access_token=" + config.MapboxApiKey)

      # Response is mapped into variable and serialised using JSON
      mapboxJsonResponse = mapboxResponse.json()
      
      # Latitude and Longitude are parsed from the JSON response
      coordinates = mapboxJsonResponse["features"][0]["geometry"]["coordinates"]

      # Setting apiCallCount to 1 to prevent further api calls for co-ordinates (unless the user changes the current location variable)
      apiCallCount = 1

   # Current longitude and latitude are mapped into variables
   longitude = coordinates[0]
   latitude = coordinates[1]

   
#longitude = -6.258265
#latitude = 53.363245

   # Obtaining current timestamp
   now = datetime.datetime.now()

   # Stripping time from current timestamp
   presentTime = datetime.datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f')
   # Setting time for daily API call for sunset sunrise API
   sunsetApiTimeDailyFetchStart = '09:00:00'
   # Declaring and initialising variable to indicate end of period each day when API should fetch information (25 second interval each day to make API call for sunset for that day)
   sunsetApiTimeDailyFetchEnd = ''
   sunsetApiTimeDailyFetchEnd += sunsetApiTimeDailyFetchStart[0:6] + (str(int(sunsetApiTimeDailyFetchStart[6:]) + 25))
   
   # Sunset Sunrise API fetch start and end period time objects declared
   sunsetApiTimeDailyFetchStartObject= datetime.datetime.strptime(sunsetApiTimeDailyFetchStart, '%H:%M:%S')
   sunsetApiTimeDailyFetchEndObject= datetime.datetime.strptime(sunsetApiTimeDailyFetchEnd, '%H:%M:%S')

   # Declaring api call counter for Sunset Sunrise API
   initialApiCall = 0
   
   # Check to see if present time is greater than the Sunset Sunrise fetch start period (09:00:00) and less than the Sunset Sunrise fetch end period (09:00:25) or if the initialApiCall variable has a value of 0
   if presentTime.time() > sunsetApiTimeDailyFetchStartObject.time() and presentTime.time() < sunsetApiTimeDailyFetchEndObject.time() or initialApiCall == 0:
      # If either condition is met, sunset for day in question is obtained from SunSet Sunrise API request
      sunsetSunriseResponse = requests.get("https://api.sunrise-sunset.org/json?lat=" + str(latitude) + "&lng=" + str(longitude) + "&formatted=0") 

      # Response is serialised with JSON
      sunsetSunriseJsonResponse = sunsetSunriseResponse.json()

      #Sunset for today is stored in sunsetToday variable (obtained from JSON response from Sunset Sunrise)
      sunsetToday = sunsetSunriseJsonResponse["results"]["sunset"]
      



   # For loop in play to obtain the luminance values from each pixel (100 pixels in the captured data stream)
   for i in range(0, 100):
         # The first 128 bytes of each pixel contain the luminance information
         for j in range(0, 128):
            
            # pixelLuminance is used to store each value in each of the 128 bytes of a single pixel
            pixelLuminance += Y[i][j]

            # count is incremented (this keeps count of current pixel count)
            count = count + 1

            # Once the final byte has been read (at 128), the average luminance for the pixel is obtained by dividing the cumulative value in pixelLuminance by 128
            if count == 128:
              # This average value is appended to the avgLuminancePerPixelArray
              avgLuminancePerPixelArray.append(pixelLuminance / 128)

              # pixelLuminance and count are reset to 0 so that they can proceed through the next iteration (next pixel of the stream data)
              pixelLuminance = 0
              count = 0

   # variable initialised that will store totalAverageLuminance
   totalAverageLuminance = 0

   # For loop iterates through the values in the avgLuminancePerPixelArray
   for eachPixel in avgLuminancePerPixelArray:
      # Each luminance value for each pixel is added to the totalAverageLuminance
      totalAverageLuminance += eachPixel

      # The current average Luminance is obtained by dividing that value by 100 (as there are 100 pixels in the data stream)
      currentAverageLuminance = totalAverageLuminance / 100

      # String used to obtain the time of sunset today
      sunsetTodayStr = sunsetToday[(sunsetToday.index('T') + 1): (sunsetToday.index('T') + 9)]
      print(sunsetTodayStr)
   
   
      # String is manipulated to obtain value that shows time of sunset today minus one hour
      oneHourBeforeSunsetTodayStr = ''
      oneHourBeforeSunsetTodayStr += (str(int(sunsetTodayStr[0:2]) - 1)) + sunsetTodayStr[2:]
      print(oneHourBeforeSunsetTodayStr)

      # Date time objects are declared for both the sunset time today and the sunset time today minus one hour times
      oneHourBeforeSunsetTodayTimeObject = datetime.datetime.strptime(oneHourBeforeSunsetTodayStr, '%H:%M:%S')
      sunsetTodayTimeObject= datetime.datetime.strptime(sunsetTodayStr, '%H:%M:%S')
      print(sunsetTodayTimeObject.time())
      print(oneHourBeforeSunsetTodayTimeObject.time())


      # Check to see if current time is less than sunset today time or current time is greater than sunset today time minus one hour (and the currentAverageLuminance is less than 100)
      if presentTime.time() > sunsetTodayTimeObject.time() or presentTime.time() > oneHourBeforeSunsetTodayTimeObject.time() and currentAverageLuminance < 100:
        # If either of these conditions are met, the isDusk variable is set to 1 (this is used by Thingspeak to determine what action should be taken)
        isDusk = 1
      else:
        # If luminance is below the threshold set of 100 but the time is not within the specified thresholds, the isDusk variable is set to 0
        isDusk = 0


      print(presentTime.time() > sunsetTodayTimeObject.time())

   #pir.wait_for_motion()
      print(pir.value)
   
      green_led.on()
   
   


   # MQTT to ThingSpeak for luminance
   channelId = "1246098"

   apiKey = config.luminanceApiKey

   mqttHost = "mqtt.thingspeak.com"

   import ssl
   tTransport = "websockets"
   tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
   tPort = 443

   # Creating MQTT topic for current luminance
   topic = "channels/" + channelId + "/publish/" + apiKey

   # If the current apiSecondCount counter is 16 (construct the payload for MQTT - contains currentaverageLuminance and isDusk variable values)
   if apiSecondCount == 16:
      tPayload="field1=" + str(currentAverageLuminance) + "&field2=" + str(isDusk)

   
      
   if apiSecondCount == 16:
      # These are published to ThingSpeak via MQTT
      publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)


   # MQTT to ThingSpeak for motion detected
   motionChannelId = "1249999"

   motionApiKey = config.motionApiKey

   mqttHost = "mqtt.thingspeak.com"

   tTransport = "websockets"
   tPortMotion = 80

   # Constructing MQTT motion topic
   motionTopic = "channels/" + motionChannelId + "/publish/" + motionApiKey
   if apiSecondCount == 16:
      #If 1 is present in arrayOfValues - it shows that motion was detected by the PIR sensor in the last 15 seconds - as a reading takes place every second
      if (1 in arrayOfValues):
         motionDetected = 1

   channelPayload="field1=" + str(motionDetected)
  
   # If the current value of apiSecondCount is 16 (the counter variable) - publish to the Thingspeak motionTopic via MQTT
   if apiSecondCount == 16:
      publish.single(motionTopic, payload=channelPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
      apiSecondCount = 0
      motionDetected = 0
      arrayOfValues = []
   

   # Program sleeps every second (MQTT pushes to ThingSpeak only occur every 16 seconds as the free tier only allows data pushes every 15 seconds)
   time.sleep(1)