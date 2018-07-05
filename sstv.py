#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import subprocess
import fcntl, sys
import datetime
import Adafruit_DHT
from PIL import Image, ImageFont, ImageDraw

mycallsign = "W5MAW"
captureresolution = "1280x720"
pisstv = '/opt/webcam/pisstv/pisstv'
pid_file = '/opt/webcam/sstv.lock'
symlink = '/opt/webcam/current.jpg'
tempfile = '/opt/webcam/sstv.jpg'

font = ImageFont.load_default()
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 24)

sensor = Adafruit_DHT.DHT22
sensorpin = 4

def main():
  fp = open(pid_file, 'w')
  try:
      fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
  except IOError:
      # another instance is running
      sys.exit(0)
      
  while (True):
    img = Image.open(symlink)
    img = img.resize((320, 256))
    draw = ImageDraw.Draw(img)
    draw.text((17, 17), mycallsign, (0, 0, 0), font=font)
    draw.text((16, 16), mycallsign, (255, 255, 255), font=font)
    draw.text((240, 17), time.strftime('%H%M'), (0, 0, 0), font=font)
    draw.text((239, 16), time.strftime('%H%M'), (255, 255, 255), font=font)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensorpin)
    draw.text((130, 17), "{:.1f}C".format(temperature), (0, 0, 0), font=font)
    draw.text((129, 16), "{:.1f}C".format(temperature), (255, 255, 255), font=font)
    img.save(tempfile)
    print(tempfile)
      
    command = "{0} {1} 22050".format(pisstv, tempfile) 
    print(command)
    subprocess.call(command, shell=True)

    wavfile = tempfile + ".wav"
    command = "aplay {0}".format(wavfile) 
    print(command)
    subprocess.call(command, shell=True)
    
    #time.sleep(120) # adjust for radio duty cycle
    
if __name__ == '__main__':
	main()
