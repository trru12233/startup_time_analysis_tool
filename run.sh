#!/bin/bash

dev="/dev/ttyUSB0"

if [ ! -c "$dev" ]; then
    echo "$dev is not exist!"
    exit 1
fi

mode=$(ls -l $dev | awk '{print $1}')
if [ x"$mode" != x"crwxrwxrwx" ]; then
    sudo chmod 777 /dev/ttyUSB0
fi

python grabserial -v -S -d $dev -t  -o log -Q
#sudo python grabserial -S -d $dev -t -o log
