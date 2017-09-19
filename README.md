# SocketPi
SocketPi is my first project for the Raspberry Pi 3.
It uses a simple 433 MHz transmitter to switch some old radio controlled
sockets.

## Switching the Sockets
For the socket switching, we use the [wiringPi](http://wiringpi.com/) C
library.

### Install Dependencies
Apart from the packages that are installed on Raspbian by default, we need
wiringPi, which is installed from git:
    sudo apt install git
    git clone git://git.drogon.net/wiringPi
    cd wiringPi
    ./build

### Analysis of Existing Sockets
The sockets are three [düwi](https://de.wikipedia.org/wiki/Düwi) model 0369-3.
They were originally controlled by a remote control with a combined on/off
button for each of the sockets (and a button for a non-existing fourth
switch and additional dimmer buttons for all four switches, which are not
used for this model without dimmer).

The remote control and the switches can be configured by a 6-bit DIP switch
to a common house code, which is set to 111111 on my devices.
Following the guide in
https://tutorials-raspberrypi.de/raspberry-pi-funksteckdosen-433-mhz-steuern/,
I found the following codes for this setting:

Socket | On/Off | Dimmer
-------|--------|-------
A      | 340    | 337
B      | 1108   | 1105
C      | 1348   | 1345
D      | 1300   | 1297

### C Program to Switch Sockets
A small C program, which sends the on/off codes to sockets numbered 1 to 4,
is implemented in socket_switch.c.
It only depends on the wiringPi library being installed and can be compiled
by:
    gcc socket_switch.c -o socket_switch -lwiringPi

## Web Interface
The sockets shall be controlled by a simple web interface created with
Python behind a Nginx web server.
We roughly follow the guide in
https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-14-04.

### Install Dependencies
First, we want to work in a Python virtual environment:
    sudo apt install python3-pip
    sudo -H pip3 install virtualenv virtualenvwrapper
We add the following at the end of .bashrc:
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export WORKON_HOME=~/PythonEnvs
    source /usr/local/bin/virtualenvwrapper.sh

We create a virtual environment for our socket project, which we can
deactivate and later reenter with the helpers from virtualenvwrapper:
    mkvirtualenv socket
    deactivate
    workon socket
    deactivate

We install uWSGI (globally, outside of virtual environments):
    sudo apt install python3-dev
    sudo -H pip3 install uwsgi

And we install Nginx as a reverse proxy in front of uWSGI:
    sudo apt install nginx-light

### Configure uWSGI and Nginx
The application resides in the socket_app.py script and should be mounted at
http://localhost/socket.

For uWSGI, we create the socket_app.ini uWSGI configuration file and a
socket_app.service systemd unit, which is linked from /etc/systemd/system/,
enabled and started:
    sudo ln -s /home/pi/socket/socket_app.service /etc/systemd/system/
    sudo systemctl enable socket_app.service
    sudo systemctl start socket_app.service

For Nginx, we create the socket_app.conf Nginx configuration file, which is
linked from /etc/nginx/sites-available/ and enabled by a symlink in
/etc/nginx/sites-enabled/ (while disabling the default site).
Finally, Nginx is restarted:
    sudo ln -s /home/pi/socket/socket_app.conf /etc/nginx/sites-available/
    sudo ln -s ../sites-available/socket_app.conf /etc/nginx/sites-enabled/
    sudo rm /etc/nginx/sites-enabled/default
    sudo systemctl restart nginx.service
