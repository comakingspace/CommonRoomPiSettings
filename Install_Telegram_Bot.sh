pip install -r /home/pi/CommonRoomPiSettings/SpaceAutomation/requirements.txt

sudo cp telegram_bot.service /etc/systemd/system/telegram_bot.service
sudo systemctl daemon-reload
sudo systemctl enable telegram_bot.service
sudo systemctl start telegram_bot.service