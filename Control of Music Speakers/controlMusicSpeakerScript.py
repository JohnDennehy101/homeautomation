# Blue dot library is used to connect Raspberry Pi to Android Phone (OnePlus 5T) - via Bluetooth
from bluedot import BlueDot
# Soco library is used to control Sonos Music Speakers
import soco
from soco.music_library import MusicLibrary
from soco.alarms import Alarm
from soco.alarms import get_alarms
from datetime import time
from signal import pause


# Set to discovery mode to discover Sonos Speakers on current network
speakers = soco.discover()
# Speaker Ip address is assigned to speakerIp variable
speakerIp = speakers.pop().ip_address

# Declaring instance of Soco object (with IP address of Sonos speaker) 
sonos_speaker = soco.SoCo(speakerIp)

print(sonos_speaker)


#device.clear_queue()
#print("New Queue")
#queue = device.get_queue()
#for item in queue:
    #print(item.title)




# Defining function to detect which blue dot button has been pressed on the Android phone
def pressed(pos):

    # If column is 1 and row is 0 - the user wants to set the weekend alarm on the speaker
    if pos.col == 1 and pos.row == 0:
        #Weekend Alarm
         print('weekend alarm')
         # Declaring instance of soco Alarm instance (using IP address of Sonos speaker)
         weekEndAlarm = Alarm(sonos_speaker)
         # First, the alarm needs to be saved before it can be configured
         weekEndAlarm.save()
         # Recurrence of the alarm is set (once as I would only want to set an alarm for the next day)
         weekEndAlarm.recurrence = "ONCE"
         # Time of alarm is set to 10 am
         weekEndAlarm.start_time = time(10, 00, 00)
         # Duration of alarm is set (5 minutes)
         weekEndAlarmduration = time(0, 5, 0)
         # Updated configuration of alarm is once again saved to the Speaker
         weekEndAlarm.save()
    # If column is 1 and row is 2 - the user wants to set the weekday alarm on the speaker
    elif pos.col == 1 and pos.row == 2:
        #work Alarm
         print('work alarm')
         # Declaring instance of soco Alarm instance (using IP address of Sonos speaker)
         weekDayAlarm = Alarm(sonos_speaker)
         # First, the alarm needs to be saved before it can be configured
         weekDayAlarm.save()
         # Recurrence of the alarm is set (once as I would only want to set an alarm for the next day)
         weekDayAlarm.recurrence = "ONCE"
         # Time of alarm is set to 8:45 am
         weekDayAlarm.start_time = time(8, 45, 00)
         # Duration of alarm is set (10 minutes)
         weekDayAlarm.duration = time(0, 10, 0)
         # Updated configuration of alarm is once again saved to the Speaker
         weekDayAlarm.save()

    # If column is 2 and row is 1 - the user wants to increase the current volume on the speaker
    elif pos.col == 2 and pos.row == 1:
         print('increase volume')
        # Increase speaker volume (by 5 percent)
         sonos_speaker.volume = sonos_speaker.volume + 5

    # If column is 1 and row is 0 - the user wants to decrease the current volume on the speaker
    elif pos.col == 0 and pos.row == 1:
         print('decrease volumem')
         # Decrease speaker volume (by 5 percent)
         sonos_speaker.volume = sonos_speaker.volume - 5
       

    # If column is 1 and row is 1 - the user wants to pause playback on the speaker
    elif pos.col == 1 and pos.row == 1:
         print('pause playback')
         # Call .pause() method to pause the speaker
         sonos_speaker.pause()
        #Pause playback

        #Muting Device
#device.volume = 0

#Clearing queue
#device.clear_queue()

    print("button {}.{} pressed".format(pos, pos.row))

# Instance of blue dot is declared (with 3 colums and 3 rows for multiple buttons)
bd = BlueDot(cols=3, rows=3)

# Hiding some buttons
bd[0,0].visible = False
bd[0,2].visible = False
bd[2,0].visible = False
bd[2,2].visible = False

# Weekend alarm button is given colour of green
bd[1,0].color = 'green'

# Weekday alarm button is given colour of red
bd[1,2].color = 'red'

# Increase and decrease volume buttons are given colour of grey
bd[0,1].color = 'gray'
bd[0,2].color = 'gray'
bd[2,1].color = 'gray'

# Call pressed function once bluedot button on Blue Dot application on Android Phone is pressed
bd.when_pressed = pressed

# Program is paused until action for that button is completed. Then blue dot sets blue dot to discovery again (waiting for additional button presses)
pause()



#print('working')
#print(device.music_library.MusicLibrary.get_music_library_information('artists', start=0, max_items=100))
#device.play_uri('http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3')
#print(device.get_current_transport_info()['current_transport_state'])