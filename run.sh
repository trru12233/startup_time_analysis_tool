#!/bin/bash

serial="/dev/ttyUSB0"
relay="/dev/ttyUSB1"

if [ ! -c "$serial" ]; then
    echo "$serial is not exist!"
    exit 1
fi

if [ ! -c "$relay" ]; then
    relay="UNUSE"
fi

mode=$(ls -l $serial | awk '{print $1}')
if [ x"$mode" != x"crwxrwxrwx" ]; then
    sudo chmod 777 /dev/ttyUSB0
fi

# python grabserial -v -S -d $serial -t  -o "log.txt" -r $relay -Q
python grabserial -v -S -d $serial -t  -o "./log/%Y-%m-%dT%H-%M-%S.txt" -r $relay -Q
#sudo python grabserial -S -d $serial -t -o log
