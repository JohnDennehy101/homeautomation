# Home Automation & Running Analysis Project

#### Student Name: John Dennehy Student ID: 20091408

#### Github Repo - https://github.com/JohnDennehy101/homeautomation

## Introduction
There are 3 different parts to my Home Automation & Running Analysis project:
- Automation of Indoor Lighting

![](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/LightSystemPictorial.png?raw=true=250x250)
![](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/currentLuminanceInformationalFlow.png?raw=true=250x250)
![](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/motionDetectedInformationalFlow.png?raw=true=250x250)

- Control of Sonos Music Speakers

![](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/musicSpeakerPictorial.png?raw=true=250x250)
![](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/musicSpeakerInformationalFlow.png?raw=true=250x250)

- Impact of Weather Conditions on Running Performance

![](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/weatherRunningPictorial.png?raw=true=250x250)
![](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/weatherRunningInformationalFlow.png?raw=true=250x250)



## Repository Structure
As there are 3 parts to my project, I have created an individual folder for each project section with the additional documentation (project proposal, project submission document and project pictorial and informational flow slides) located at the root of the repository.

- Automation of Indoor Lighting - **'Automation of Lighting'** folder
- Control of Sonos Music Speakers - **'Control of Music Speakers'** folder
- Impact of Weather Conditions on Running Performance - **'Weather_Running_Performance_Analysis'** folder

As I only have 1 Raspberry Pi (and each of the above project components requires a different program, I tested each program at different times).

## Goals
**1. Automation of Lighting - Luminance Analysis using Picamera (Turning on Kasa Plug)**

The aim with this section of the project was to automate the process of turning on a light in my room (when it is dark in the room and it is evening time).
The Picamera was used to capture an analysis of current light levels in the room (luminance).
A 3rd party API (Sunrise Sunset) was used to determine the predicted time of dusk each day.
After some analysis, the 'currentLuminance' and 'isDusk' values were pushed to Thingspeak.
If it is dark in the room (based on currentLuminance threshold) and 'isDusk' equals 1, a Thingspeak React triggered an IFTTT webhook that turned on the Kasa smart plug in the room (lamp is plugged into this plug).

**2. Automation of Lighting - Luminance Analysis using Picamera (Triggering Email Alert)**

If it is dark in the room but it is not evening time, I wanted to receive an email telling me to turn on the light.
If it is dark in the room (based on currentLuminance threshold) and 'isDusk' equals 0, a Thingspeak React triggered an IFTTT webhook that emailed me telling me to turn on the light.

**3. Automation of Lighting - Motion Detection Using PIR Sensor**

I wanted to automate turning on a light in my kitchen (which always requires artificial light). A PIR motion sensor was used to detect motion. If motion was detected in the previous 15 seconds, a ThingSpeak React triggered an IFTTT webhook that turned on another Kasa smart plug in the kitchen (light is plugged into this plug).

**4. Control of Sonos Music Speakers**

The only way to control my Sonos music speakers was via applications that used Wifi as the main method of communication (Sonos Android App / Spotify).
I had intermittent issues where the connection was not functioning correctly between the applications and the speaker.
I therefore wanted an alternative means of controlling the speaker.
Bluetooth on my phone (via BlueDot Android application) and Bluetooth on the Raspberry Pi were used in conjunction with the Soco Python library to offer an alternative method of controlling the speaker.

**5. Impact of Weather Conditions on Running Performance**

I run regularly and receive stats on my running performance through Garmin and Strava Android applications. However, I believed these were not providing a rich enough analysis as detailed weather conditions are not included in this data.

Therefore, I used a combination of weather data from the SenseHat and OpenWeather API to determine current weather conditions.
Firebase was used to ensure persistence of data.
The Strava API was used to provide data for the latest activity (and detect new activities).
A Glitch application was used to provide a friendly user interface for viewing the analysis (Chart.js and Google Maps API were used to enhance app functionality), thereby providing a means of viewing key stats from the latest activity with weather conditions for the last hour.

On detection of a new activity, I received an SMS message with a link to the Glitch application (via Twilio's API) to enhance the user experience and ensure that the application was easily accessible.



## Overview - Automation of Light System

Raspberry Pi with PiCamera for image analysis and PIR motion sensor connected via breadboard

![picamera](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/PiMotionSensorCamera.jpg?raw=true=250x250)

**1. Automation of Lighting - Luminance Analysis using Picamera (Turning on Kasa Plug)**\
[Youtube Video (Duration 4:46)](https://youtu.be/V9ObKrVNxlw)

The Raspberry Picamera was used to take YUV images on a regular basis so that an analysis could be undertaken on the Y (luminance) section of the stream. Every 16 seconds (due to Thingspeak's free tier restriction of data pushes at a 15 second interval), the average luminance was published to the currentLuminance Thingspeak channel via MQTT.

![currentLuminanceChart](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/currentLuminanceThingSpeakChannel.png?raw=true)

A second value 'isDusk' was also pushed to the /currentLuminance channel. This was either 0 (it should not be dark yet - not dusk - obtained via an API call to Sunrise Sunset) or 1 (current time is greater than the 'dusk' time obtained from the API call to Sunrise Sunset

![isDuskChart](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/currentLuminanceIsDusk.png?raw=true)

Both the 'currentLuminance' and 'isDusk' values were fed to a Matlab analysis in a separate 'currentLuminanceActionDetermined' channel.
As can be seen below, the value of 'currentLuminance' and 'isDusk' determined the 'action' value.
![MatLabChart](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/MatLabAnalysis.png?raw=true)

If current luminance was below 130 and isDusk == 1 (it is dark in the room and it is evening time - analysis determined in Python program by comparing current time against API response from Sunrise Sunset), action was set to 2. I created a React for this condition.

![action2](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/currentLuminanceActionDetermined.png?raw=true)
![duskreact](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/DuskReact.png?raw=true)

The React triggered a Thing HTTP (IFTTT webhook) to turn on the Kasa Smart Plug.

![duskifttt](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/IFTTTTurnOnLight.png?raw=true)

Kasa Smart Plug (Before webhook)

![kasasmartplugoff](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/KasaLivingRoom.png?raw=true)

Kasa Smart Plug (After webhook)

![kasasmartplugon](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/KasaLivingRoomlampOn.png?raw=true)





**2. Automation of Lighting - Luminance Analysis using Picamera (Triggering Email Alert)**\
[Youtube Video (Duration 3:29)](https://youtu.be/VFEnA1YMHIs)

If current luminance was below 130 and isDusk == 0 (it is dark in the room and it is not evening time - analysis determined in Python program by comparing current time against API response from Sunrise Sunset), action was set to 1. I created a React for this condition.

![action1](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/currentLuminanceActionDetermined1.png?raw=true)
![notduskreact](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/NotDuskReact.png?raw=true)

The React triggered a Thing HTTP (IFTTT webhook) to email me telling me that it is dark in the room and that I should turn on the light.

![notduskifttt](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/IFTTTEmailWebhookOverview.png?raw=true)


Email Sent on Webhook Trigger

![notduskiftttemail](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/IFTTTEmailWebhook.png?raw=true)

**3. Automation of Lighting - Motion Detection Using PIR Sensor**\
[Youtube Video (Duration 3:38)](https://youtu.be/C8Rj6ve0Dhw)

A PIR motion sensor was used to detect motion in the room (connected to Raspberry Pi with breadboard). The value of the GPIO pin was read every second and appended to an array (0 for no motion detected, 1 for motion detected). At a 16 second interval, a check was made on the array to see if a 1 was present in the array (i.e. motion had been detected in the previous 15 seconds). If 1 was present, 'pinStatus' was set to 1 and pushed to Thingspeak via MQTT. If 1 was not present in the array, no motion was detected in the previous 15 seconds and the 'pinStatus' was set to 0 and pushed to Thingspeak via MQTT.

This was only pushed at a 16 second interval due to the restrictions on Thingspeak's free tier.

motionDetectedKitchen ThingSpeak channel

![motionDetectedKitchenThingspeak](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/motionDetectedKitchenThingSpeak.png?raw=true)

I created a react on this value (if the value pushed was 1, motion had been detected in the previous 15 seconds and the light should be turned on).

![motionDetectedKitchenThingspeakReact](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/motionDetectedKitchenReact.png?raw=true)

The React triggered a Thing HTTP (IFTTT webhook) to turn on the Kasa Smart plug (a lamp was plugged into this plug).

![motionDetectedKitchenThingspeakHTTP](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/motionDetectedKitchenIFTTT.png?raw=true)

Kasa Smart Plug (Before webhook)

![kitchenlightoff](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/KasaKitchenLightOff.png?raw=true)


Kasa Smart Plug (After webhook)

![kitchenlighton](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/KasaKitchenLightOn.png?raw=true)






## Overview - Control of Music Speakers
[Youtube Video (Duration 3:49)](https://youtu.be/NlQggL6Z9zg)

The BlueDot Android application was used to initiate and establish a Bluetooth connection between my OnePlus 5T and the Raspberry Pi.
Each button was configured for a specific action. The Soco Python library was used to complete the relevant action on the Sonos Speaker.

* Left Grey Button - used to decrease volume on the Sonos speaker by 5%
* Right Grey Button - used to increase volume on the Sonos speaker by 5%
* Green Button - used to set a weekend alarm on the Sonos speaker (10:00:00AM)
* Red Button - used to set a weekday alarm on the Sonos speaker (08:45:00AM)
* Blue Button - used to pause/play playback on the Sonos speaker

![bluedot](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/BluedotAndroidApp.png?raw=true)

## Overview - Impact of Weather Conditions on Running Performance
[Youtube Video (Duration 5:04)](https://youtu.be/C_OercAVljs)

Both the Sense Hat and a third-party API (OpenWeather) were used to obtain weather data. This data was pushed to Firebase at a 2 minute interval.

Raspberry Pi with Sense Hat linked to mini black hat hack3r to ensure accurate weather data readings

![piweather](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/PiSenseHatMiniBlackHatHackr.jpg?raw=true=250x250)

The Strava API was polled at a 10 second interval to determine if a new activity had been added (by comparing the length of the first API response against the second). If there was a difference in length, the API response was sorted by date (to ensure the latest activity was pushed) and the data for the latest activity was pushed to Firebase.

![firebase](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/firebase.png?raw=true)

If a new activity was detected, the Twilio SMS API was used to send a message to my phone informing me that a new activity had been uploaded to Strava (with a link to the Glitch application dashboard).

![twilio](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/TwilioText.png?raw=true)

I completed the Glitch application to provide a user-friendly interface for viewing both the weather and latest activity data.

[Glitch Application Link](https://weather-impact-on-running-performance.glitch.me/)

As the Strava API response includes a polyline of the GPS activity route, I decided to integrate Google maps onto the dashboard to display the activity polyline (with map markers added for activity start and end latitude and longitude).

![googlemaps](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/GlitchAppMap.png?raw=true)

I also used Chart.js to show activity trends over time.

![chartjsrun](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/GlitchAppRunTrend.png?raw=true)

A number of Chart.js charts were also used to display the different weather data points for the last hour (by limiting Firebase to the last 30 records in the 'weatherData' reference - as weather data was pushed to Firebase at a 2 minute interval).

![chartjsweather](https://github.com/JohnDennehy101/homeautomation/blob/master/readme_images/GlitchAppWeatherCharts.png?raw=true)









