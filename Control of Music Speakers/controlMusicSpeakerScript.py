from bluedot import BlueDot
import soco
from soco.music_library import MusicLibrary
#from soco.alarm import Alarm
from soco.alarms import Alarm
from soco.alarms import get_alarms
from datetime import time
from signal import pause



speakers = soco.discover()
speakerIp = speakers.pop().ip_address


sonos_speaker = soco.SoCo(speakerIp)

print(sonos_speaker)


def pressed(pos):
    if pos.col == 1 and pos.row == 0:
        #Weekend Alarm
         print('weekend alarm')
         weekEndAlarm = Alarm(sonos_speaker)
         weekEndAlarm.save()
         weekEndAlarm.recurrence = "ONCE"
         weekEndAlarm.start_time = time(10, 00, 00)
         weekEndAlarmduration = time(0, 5, 0)
         weekEndAlarm.save()
    elif pos.col == 1 and pos.row == 2:
        #work Alarm
         print('work alarm')
         weekDayAlarm = Alarm(sonos_speaker)
         weekDayAlarm.save()
         weekDayAlarm.recurrence = "ONCE"
         weekDayAlarm.start_time = time(8, 45, 00)
         weekDayAlarm.duration = time(0, 10, 0)
         weekDayAlarm.save()
    elif pos.col == 2 and pos.row == 1:
         print('increase volume')
        #Increase volume
         sonos_speaker.volume = sonos_speaker.volume + 5
    elif pos.col == 0 and pos.row == 1:
         print('decrease volumem')
         sonos_speaker.volume = sonos_speaker.volume - 5
        #Decrease volume
    elif pos.col == 1 and pos.row == 1:
         print('pause playback')
         sonos_speaker.pause()
        #Pause playback

        #Muting Device
#device.volume = 0

#Clearing queue
#device.clear_queue()

    print("button {}.{} pressed".format(pos, pos.row))

bd = BlueDot(cols=3, rows=3)
bd[0,0].visible = False
bd[0,2].visible = False
bd[2,0].visible = False
bd[2,2].visible = False
bd[1,0].color = 'green'
bd[1,2].color = 'red'
bd[0,1].color = 'gray'
bd[0,2].color = 'gray'
bd[2,1].color = 'gray'
bd.when_pressed = pressed


pause()



#print('working')
#print(device.music_library.MusicLibrary.get_music_library_information('artists', start=0, max_items=100))
#device.play_uri('http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3')
#print(device.get_current_transport_info()['current_transport_state'])