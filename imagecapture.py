#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import subprocess
import fcntl, sys
import datetime

captureresolution = "1280x720"
pid_file = '/opt/webcam/imagecapture.lock'
symlink = '/opt/webcam/current.jpg'

def captureImage():
	filename = "/opt/webcam/images/{0}.jpg".format(int(time.time()) + 15)
	command = "fswebcam --no-banner -S 150 --fps 15 -p YUYV -r {0} {1}".format(captureresolution, filename) 
	print(command)
	subprocess.call(command, shell=True)
	return filename

def main():
  fp = open(pid_file, 'w')
  try:
      fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
  except IOError:
      # another instance is running
      sys.exit(0)
      
  while (True):
    now = datetime.datetime.now()
    if now.second > 50 or now.second < 55 or now.second > 20 or now.second < 25:
      # five second grace period at 0 and 30 (-15 because of image capture delay)
      filename = captureImage()
      command = "ln -s {0} {1}_tmp && mv -Tf {1}_tmp {1}".format(filename, symlink)
      print(command)
      subprocess.call(command, shell=True)
      
      time.sleep(20)
    else:
      time.sleep(0.5)

if __name__ == '__main__':
	main()
