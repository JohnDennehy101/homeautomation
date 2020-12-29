# Home Automation & Running Analysis Project

#### Student Name: John Dennehy Student ID: 20091408

#### Github Repo - https://github.com/JohnDennehy101/homeautomation

## Introduction
There are 3 different parts to my Home Automation & Running Analysis project:
- Automation of Indoor Lighting
- Control of Sonos Music Speakers
- Impact of Weather Conditions on Running Performance

## Repository Structure
As there are 3 parts to my project, I have created an individual folder for each project section with the additional documentation (project proposal, project submission document and project pictorial and informational flow slides) located at the root of the repository.

- Automation of Indoor Lighting - **'Automation of Lighting'** folder
- Control of Sonos Music Speakers - **'Control of Music Speakers'** folder
- Impact of Weather Conditions on Running Performance - **'Weather_Running_Performance_Analysis'** folder

As I only have 1 Raspberry Pi (and each of the above project components requires a different program, I tested each program at different times).

## Overview - Automation of Light System
**1. Automation of Lighting - Luminance Analysis using Picamera (Turning on Kasa Plug)**\
[Youtube Video (Duration 4:46)](https://youtu.be/V9ObKrVNxlw)

The Raspberry Picamera was used to take YUV images on a regular basis so that an analysis could be undertaken on the Y (luminance) section of the stream. Every 16 seconds (due to Thingspeak's free tier restriction of data pushes at a 15 second interval), the average luminance was published to the currentLuminance Thingspeak channel via MQTT.

A second value 'isDusk' was also pushed to the /currentLuminance channel. This was either 0 (it should not be dark yet - not dusk - obtained via an API call to Sunrise Sunset) or 1 (current time is greater than the 'dusk' time obtained from the API call to Sunrise Sunset



**2. Automation of Lighting - Luminance Analysis using Picamera (Triggering Email Alert)**\
[Youtube Video (Duration 3:29)](https://youtu.be/VFEnA1YMHIs)

**3. Automation of Lighting - Motion Detection Using PIR Sensor**\
[Youtube Video (Duration 3:38)](https://youtu.be/C8Rj6ve0Dhw)

## Overview - Control of Music Speakers
[Youtube Video (Duration 3:49)](https://youtu.be/NlQggL6Z9zg)

## Overview - Impact of Weather Conditions on Running Performance
[Youtube Video (Duration 5:04)](https://youtu.be/C_OercAVljs)

