# pinergy

An energy cost display for OpenEnergyMonitor

## Hardware

- Raspberry Pi 3A+

- Pimoroni Rainbow Hat

## Software

- Raspberry Pi OS Lite 64 bit

- Pimoroni Rainbow Hat Python library - `sudo apt install python3-rainbowhat`

- Python 3 MQTT library - `sudo apt install python3-paho-mqtt`



## Creating the service

Create a file as `/etc/systemd/system/pinergy.service` containing the following:

```ini
[Unit]
Description=Pinergy
After=network.target
[Service]
ExecStart=/usr/bin/python3 -u pinergy.py
WorkingDirectory=/home/pi/scripsi/pinergy
Restart=always
User=pi
[Install]
WantedBy=multi-user.target
```

Then enable it to run at startup:

```shell
sudo systemctl enable pinergy.service
```

To control the service you can use the following commands:

```shell
sudo systemctl stop pinergy.service
sudo systemctl start pinergy.service
```
