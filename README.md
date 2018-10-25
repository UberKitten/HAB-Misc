# HAB-Misc
Miscellaneous scripts used for high altitude ballooning

## Webcam

I recommend storing the binaries in /opt/webcam

Prereq: 
````
sudo mkdir /opt/webcam
sudo chown -R astra:astra .
cd /opt/webcam
mkdir images
sudo apt install fswebcam libjpeg-dev zlib1g-dev python-dev libgd2-xpm-dev libmagic-dev
virtualenv env
source env/bin/activate
pip install Pillow

git clone https://github.com/AgriVision/pisstv.git
cd pisstv/
gcc -lm -lgd -lmagic -o pisstv pisstv.c

cd
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
chmod +x setup.py
python setup.py install
````
Finally set up your crontab and udev like the example files.
