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
import config

width = 100
height = 100
green_led = LED(17)
pir = MotionSensor(4)
green_led.off()

arrayOfValues = []
apiSecondCount = 0
motionDetected = 0

while True:
   apiSecondCount+= 1
   arrayOfValues.append(pir.value)

   stream = open('image.data', 'w+b')
# Capture the image in YUV format
   with picamera.PiCamera() as camera:
      camera.resolution = (width, height)
      camera.start_preview()
      time.sleep(2)
      camera.capture(stream, 'yuv')
# Rewind the stream for reading
      stream.seek(0)
# Calculate the actual image size in the stream (accounting for rounding
# of the resolution)
      fwidth = (width + 31) // 32 * 32
      fheight = (height + 15) // 16 * 16
# Load the Y (luminance) data from the stream
      Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
         reshape((fheight, fwidth))
# Load the UV (chrominance) data from the stream, and double its size
   avgLuminancePerPixelArray = []
   pixelLuminance = 0
   count = 0
   print(len(Y))

#for x in Y:
 # print(x)


#API call to Mapbox to receive longitude and latitude for current location
   currentLocation = "Drumcondra"
   apiCallCount = 0

   if (currentLocation.upper() != "DRUMCONDRA" or apiCallCount == 0):

      mapboxResponse = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/" + currentLocation + ".json?access_token=" + config.motionApiKey)

      mapboxJsonResponse = mapboxResponse.json()

      coordinates = mapboxJsonResponse["features"][0]["geometry"]["coordinates"]
      apiCallCount = 1
   longitude = coordinates[0]
   latitude = coordinates[1]

   
#longitude = -6.258265
#latitude = 53.363245
   now = datetime.datetime.now()
   presentTime = datetime.datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f')
   sunsetApiTimeDailyFetchStart = '09:00:00'
   sunsetApiTimeDailyFetchEnd = ''
   sunsetApiTimeDailyFetchEnd += sunsetApiTimeDailyFetchStart[0:6] + (str(int(sunsetApiTimeDailyFetchStart[6:]) + 25))
  
   sunsetApiTimeDailyFetchStartObject= datetime.datetime.strptime(sunsetApiTimeDailyFetchStart, '%H:%M:%S')
   sunsetApiTimeDailyFetchEndObject= datetime.datetime.strptime(sunsetApiTimeDailyFetchEnd, '%H:%M:%S')
   initialApiCall = 0

   if presentTime.time() > sunsetApiTimeDailyFetchStartObject.time() and presentTime.time() < sunsetApiTimeDailyFetchEndObject.time() or initialApiCall == 0:
      sunsetSunriseResponse = requests.get("https://api.sunrise-sunset.org/json?lat=" + str(latitude) + "&lng=" + str(longitude) + "&formatted=0") 
      sunsetSunriseJsonResponse = sunsetSunriseResponse.json()
      sunsetToday = sunsetSunriseJsonResponse["results"]["sunset"]
      




    
#for x in Y:
   
   for i in range(0, 100):

         for j in range(0, 128):
        
            pixelLuminance += Y[i][j]
            count = count + 1
            if count == 128:
              avgLuminancePerPixelArray.append(pixelLuminance / 128)
              pixelLuminance = 0
              count = 0

   
   totalAverageLuminance = 0
   for eachPixel in avgLuminancePerPixelArray:
      totalAverageLuminance += eachPixel

      currentAverageLuminance = totalAverageLuminance / 100


      sunsetTodayStr = sunsetToday[(sunsetToday.index('T') + 1): (sunsetToday.index('T') + 9)]
      print(sunsetTodayStr)
   
   

      oneHourBeforeSunsetTodayStr = ''
      oneHourBeforeSunsetTodayStr += (str(int(sunsetTodayStr[0:2]) - 1)) + sunsetTodayStr[2:]
      print(oneHourBeforeSunsetTodayStr)


      oneHourBeforeSunsetTodayTimeObject = datetime.datetime.strptime(oneHourBeforeSunsetTodayStr, '%H:%M:%S')
      sunsetTodayTimeObject= datetime.datetime.strptime(sunsetTodayStr, '%H:%M:%S')
      print(sunsetTodayTimeObject.time())
      print(oneHourBeforeSunsetTodayTimeObject.time())



      if presentTime.time() > sunsetTodayTimeObject.time() or presentTime.time() > oneHourBeforeSunsetTodayTimeObject.time() and currentAverageLuminance < 100:
        isDusk = 1
      else:
        isDusk = 0


      print(presentTime.time() > sunsetTodayTimeObject.time())

   #pir.wait_for_motion()
      print(pir.value)
   
      green_led.on()
   
   

#print(currentAverageLuminance)
      #print(test)
   # for y in test:
     # print(y)
   #for singlePixel in x:
        #print(singlePixel)
  
#print(Y)
   #MQTT to ThingSpeak for luminance
   channelId = config.channelId;

   apiKey = config.apiKey;

   mqttHost = config.mqttHost

   import ssl
   tTransport = "websockets"
   tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
   tPort = 443

   topic = "channels/" + channelId + "/publish/" + apiKey
   if apiSecondCount == 16:
      tPayload="field1=" + str(currentAverageLuminance) + "&field2=" + str(isDusk)

   
      
   if apiSecondCount == 16:
      publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)


   #MQTT to ThingSpeak for motion detected
   motionChannelId = config.motionChannelId;

   motionApiKey = config.motionApiKey;

   mqttHost = config.mqttHost

   tTransport = "websockets"
   #tTLSMotion = None
   tPortMotion = 80

   motionTopic = "channels/" + motionChannelId + "/publish/" + motionApiKey
   if apiSecondCount == 16:
      if (1 in arrayOfValues):
         motionDetected = 1

   channelPayload="field1=" + str(motionDetected)
  

   if apiSecondCount == 16:
      publish.single(motionTopic, payload=channelPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
      apiSecondCount = 0
      motionDetected = 0
      arrayOfValues = []
   


   time.sleep(1)


  







   



