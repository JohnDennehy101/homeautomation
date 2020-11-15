# Home Automation & Running Analysis Project
#### Student Name: *John Dennehy*   Student ID: *20091408*

## Introduction
There are 3 different parts to my Home Automation & Running Analysis project:
- Automation of Indoor Lighting
- Control of Sonos Music Speakers
- Study of Impact (if any) of Weather Conditions on Running Performance

As I only have 1 Raspberry Pi (and each of the above proposals requires a different program, I will be testing each program at different times).


## Description - Automation of Light System
The idea for my project is to automate certain activities in my house that are currently manual (e.g. switching on the light in my sitting room when it is dark outside, switching on the light in my kitchen when a person is present as the room is always too dark and requires artificial light).

The first part of my project will implement an automation system for turning on the light in my sitting room when it is dark outside. 

My proposal for this piece of the project is to use the MQTT protocol to publish the current luminance (via a calculation of current average luminance from analysis of unencoded image capture on Raspberry Pi Camera Module V2) via a /currentLuminance topic.
The first value will contain the current luminance.
The second value will contain a boolean 'isDusk'.

This second value will be set via two API calls:
The first API call will be to Mapbox to get the current latitude and longitude for my current address.
The latitude and longitude returned from that call will be used as parameters in the Sunrise Sunset API.
This will provide a response with the time of sunset for the day in question.
If the luminance is below the threshold where the light should be displayed (to be determined via testing) and the current time is within a certain period of the sunset time for a given day, the value will be set to True.

I will create a channel on ThingSpeak to subscribe to this information.
A check will be in place to see if current luminance is below the threshold where artificial light is not required and the second parameter is True.
If both of these conditions are met, a ThingHTTP on ThingSpeak will trigger a IFTTT webhook which will fire the event to Kasa to turn on the smart plug in the living room (which the lamp is plugged into).
If only the luminance condition is met, an email will be sent to my personal email telling me to turn the lights on.

The second part of this piece of this project will implement functionality to automatically turn on the light in my kitchen when a person is present (via a Raspberry Pi motion detector PIR).

My proposal for this piece of the project is to use the MQTT protocol to publish the current status of the sensor pin of the motion detector PIR (via a check to see if the status has changed) via a /motionDetectedKitchen topic.
The value sent to ThingSpeak will contain the status of the sensor pin.

I will create a channel on ThingSpeak to subscribe to this information.
If a change in the sensor pin is detected, a ThingHTTP on ThingSpeak will trigger a IFTTT webhook which will fire the event to Kasa to turn on the smart plug in the kitchen (which the lamp is plugged into).

## Tools, Technologies and Equipment - Automation of Light System
* Raspberry Pi4
* Raspberry Pi Camera Module V2
* MQTT (broker.hivemq.com)
* IFTTT
* 2 TP-Link Kasa Smart Wi-Fi Plugs
* Raspberry Pi Motion Detector PIR
* ThingSpeak
* Python3
* Visual Studio Code
* Visual Studio Code - Remote - SSH Extension


## Description - Control of Sonos Music Speakers
My proposal for this part of the project is to use the Bluetooth protocol on my Android Phone (OnePlus 5T) via the Blue Dot Android application to pair my phone with the Raspberry Pi (via the bluedot Python library) in order to control the Sonos speakers in my house (via button clicks in the Android application).
These speakers can already be controlled via WiFi but the connection to the speakers can be intermittent (and take some time to resolve once the issue occurs) so I want to develop an alternative solution to connect to the speakers when the WiFi connection to the speakers isn't functioning perfectly.

The 'SoCo' Python library offers the capability to control Sonos speakers (via the IP address of each speaker) to complete different actions (Play Music, Setting volume, Stopping Music etc.) The IP address of each Sonos speaker will need to be obtained and then passed to the 'SoCo' library to complete an action (based on the button that has been clicked on the Blue Dot Android application on my phone).

## Tools, Technologies and Equipment - Control of Sonos Music Speaker
* Raspberry Pi4
* OnePlus 5T
* Bluetooth Protocol
* Blue Dot Android Application
* 2 Sonos Play One Speakers
* 'bluedot' Python Library
* 'SoCo' Python Library
* Python3
* Visual Studio Code
* Visual Studio Code - Remote - SSH Extension

## Description - Study of Impact (if any) of Weather Conditions on Running Performance
My proposal for this part of the project is to determine if weather conditions have an impact on my running performance. 
I run a regular route so a crude comparison of different runs will be possible. I currently use a Garmin Forerunner 645M sports watch to track key stats on my runs.The data is pushed to Garmin Connect via Bluetooth on my OnePlus 5T. This triggers the push to Strava. As the Bluetooth on my phone is always on, data from Strava will be available 5-10 minutes after completion of the activity.

The environmental sensors on the Sense HAT will collect the weather information (heat of raspberry Pi will be taken into account in the analysis).
Requests to the Strava API will be used to obtain the activity data for runs that I have completed.
The API will be called at a specific interval (yet to be determined) to check if a new activity has been completed.
If a new activity has been completed (by checking the number of activites contained in the response with the old response), certain parts of the activity data will be pushed to Firebase (moving time, distance etc.).
The environmental data (adjusted to take account of raspberry Pi heat) will be regularly pushed to Firebase Realtime Database.
This information will also be available on a Firebase dashboard via the web application functionality offered by Firebase.
An analysis will be undertaken of the data so that it will be possible to see if there is any correlation between weather conditions and running performance.


## Tools, Technologies and Equipment - Study of Impact (if any) of Weather Conditions on Running Performance
* Raspberry Pi4
* Garmin Forerunner 645M Watch
* OnePlus 5T
* Strava API
* Firebase Realtime Database
* Firebase Web Application
* Sense HAT
* Python3
* JavaScript
* HTML5
* Visual Studio Code
* Visual Studio Code - Remote - SSH Extension


