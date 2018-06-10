#!/bin/sh
check_iqaudio_activated() {
if grep -q -E "^(device_tree_overlay|dtoverlay)=([^,]*,)*iqaudio-dacplus?(,.*)?$" /boot/config.txt ; then
  #line is available and activated
  return 0
else
  #line not available or not activated
  return 1
fi
}

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

toggle_setting_on_off()
{
lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=False
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=True
  end
  print(line)
end
if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}

enable_wifi_ap()
{
#This will be needed in a later version, when the pi should open a Wifi AP.
sudo apt-get -qq -y  install dnsmasq hostapd >> /dev/null
NOW=$(date +"%m_%d_%Y")
sudo cp /etc/dhcpcd.conf /etc/dhcpcd_$NOW.conf.bak
sudo echo "interface wlan0" > /etc/dhcpcd.conf
sudo echo "static ip_address=10.0.0.1/24" >> /etc/dhcpcd.conf
sudo service dhcpcd restart
sudo cp /etc/dnsmasq.conf /etc/dnsmasq_$NOW.conf.bak  
sudo echo "interface=wlan0" > /etc/dnsmasq.conf
sudo echo "dhcp-range=10.0.0.1,10.0.0.255,255.255.255.0,24h" >> /etc/dnsmasq.conf

sudo echo "interface=wlan0" > /etc/hostapd/hostapd.conf
#sudo echo "driver=rtl8192cu" >> /etc/hostapd/hostapd.conf
sudo echo "ssid=PiMusicbox" >> /etc/hostapd/hostapd.conf
sudo echo "hw_mode=g" >> /etc/hostapd/hostapd.conf
sudo echo "channel=6" >> /etc/hostapd/hostapd.conf
sudo echo "macaddr_acl=0" >> /etc/hostapd/hostapd.conf
sudo echo "auth_algs=1" >> /etc/hostapd/hostapd.conf
sudo echo "ignore_broadcast_ssid=0" >> /etc/hostapd/hostapd.conf
sudo echo "wpa=2" >> /etc/hostapd/hostapd.conf
sudo echo "wpa_passphrase=12345678" >> /etc/hostapd/hostapd.conf
sudo echo "wpa_key_mgmt=WPA-PSK" >> /etc/hostapd/hostapd.conf
sudo echo "wpa_pairwise=TKIP" >> /etc/hostapd/hostapd.conf
sudo echo "rsn_pairwise=CCMP" >> /etc/hostapd/hostapd.conf

sudo cp /etc/default/hostapd /etc/default/hostapd_$NOW.bak  
sudo echo "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"" > /etc/default/hostapd

sudo systemctl start hostapd
sudo systemctl start dnsmasq
}

BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf
CONFIG=/boot/config.txt
#Let us do some basic config
echo '--------------------------------------------'
echo 'First, we need to do some basic settings...'
echo 'Expand the FS'
sudo raspi-config nonint do_expand_rootfs >> /dev/null
echo 'boot to command line'
sudo raspi-config nonint do_boot_behaviour B1
echo 'Change the hostname'
sudo raspi-config nonint do_hostname CoMakingController
sudo cp interfaces.txt /etc/network/interfaces
#Right now, alsa does not need to be adjusted, since the built in sound card of the RPi supports hardware mixing.
#echo 'adjust the ALSA config.'
#sudo cp asound.conf /etc/asound.conf

#Enable the x400 expansion board
#echo '--------------------------------------------'
#echo 'Now we will enable the x400 expansion board by enabling i2c and adding a device tree overlay'
#echo 'In addition, asound.conf gets copied in order to enable software mixing in ALSA.'
#sudo raspi-config nonint do_i2c 0

#if check_iqaudio_activated ; then
 #do nothing
# echo 'iqaudio already activated'
#else
# echo 'activating iqaudio'
# enter_full_setting dtoverlay=iqaudio-dacplus $CONFIG
# sudo cp asound.conf /etc/asound.conf
#fi
#echo 'iqaudio activated'

echo 'We will anable automounting of USB Devices now'
sudo apt-get -qq install usbmount >>/dev/null
sudo mkdir -p /usbdrives/{usb0,usb1,usb2,usb3,usb4,usb5,usb6,usb7}
sudo cp usbmount.conf /etc/usbmount/usbmount.conf
#This is bad! but according to https://github.com/rbrito/usbmount/issues/2 we have to do this in order to enable usbmount on Rasbian stretch
sudo cp systemd-udevd.service /lib/systemd/system/systemd-udevd.service
sudo systemctl daemon-reload
sudo systemctl restart systemd-udevd


echo '--------------------------------------------'
echo 'Since this is intended to run on a pi3 with active Wifi, an SSH parameter needs to be set in order to ensure good ssh performance'
enter_full_setting 'IPQoS 0x00' /etc/ssh/ssh_config
enter_full_setting 'IPQoS 0x00' /etc/ssh/sshd_config
sudo systemctl restart ssh

#this would change our default shell to zsh - temporarily disabled.
#echo 'We will change our default shell to zsh'
#sudo apt-get -qq install zsh >> /dev/null
#chsh -s /bin/zsh
#echo 'And also install the OhMyZSH Customization for zsh'
#curl -s https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sudo bash

#echo '--------------------------------------------'
#echo 'Let us enable the pi to run as a wifi Access point'
#enable_wifi_ap


echo '--------------------------------------------'
echo 'System Settings changed, a reboot is recommended.'