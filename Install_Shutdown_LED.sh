#!/bin/sh

enter_full_setting()
{
lua - "$1" "$2" <<EOF > "$2.bak"
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
local made_change=False
for line in file:lines() do
  if line:match("^#?%s*"..key) then
    line=key
    made_change=True
  end
  print(line)
end
if not made_change then
  print(key)
end
EOF
mv "$2.bak" "$2"
}

echo 'enable UART to enable the power indicator LED'
enable_full_setting enable_uart=1 $CONFIG

echo 'writing python listener for power button'
sudo mkdir /opt/powerbutton
sudo cat > /opt/powerbutton/listen-for-shutdown.py << EOF
# listen to a power-button on Pin 5 (SCL)
# based on:
# https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi

import RPi.GPIO as GPIO
import subprocess


GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(3, GPIO.FALLING)

print('Power Down')
subprocess.call(['shutdown', '-h', 'now'], shell=False)
EOF

echo 'writing systemd service for power button'
sudo cat > /etc/systemd/system/listen-for-shutdown.service << EOF
[Unit]
Description=Monitor the power-button and shutdown if pressed 

[Service]
ExecStart=/usr/bin/python -u /opt/powerbutton/listen-for-shutdown.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo 'start and enable systemd service for power button'
sudo systemctl daemon-reload
sudo systemctl enable listen-for-shutdown.service
sudo systemctl start listen-for-shutdown.service