#!/bin/bash
echo "Welcome to the rapid-pro-connector automated installer"
echo "Creating rapid-pro-connector service...."

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

#echo text > installer.txt
FILENAME="/lib/systemd/system/connector.service"
touch $FILENAME

DESTDIR=$FILENAME
declare -a TEXT=("[Unit]"
                "Description=Connector service that sends data from openmrs to rapid pro and enables sms transmissions to mobile phones"
                "After=multi-user.target"
                "[Service]"
                "Type=idle"
                "ExecStart=/usr/bin/python /home/admin/connector/Rapidpro_connector/connector.py"
                "[Install]"
                "WantedBy=multi-user.target"
)


if [ -f "$DESTDIR" ]
then
    echo "Creating service file in /lib/systemd/connector.service"
    for i in "${TEXT[@]}"
        do
            echo "$i" >>  $DESTDIR
        done
    sudo chmod 644 /lib/systemd/system/connector.service
    sudo systemctl daemon-reload
    sudo systemctl enable connector.service
   

    echo "Attempting to start connector service..."
    
        systemctl restart connector.service
        journalctl -u connector.service
        sudo systemctl status connector.service
    
else 
    echo "An error ooccured while creating service file. Contact developer"
fi

