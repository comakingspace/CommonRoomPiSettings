
mkdir ~/crontab-ui
cd ~/crontab-ui
npm install crontab-ui

sudo cp crontab-ui.service /etc/systemd/system/crontab-ui.service
sudo systemctl daemon-reload
sudo systemctl enable crontab-ui.service
sudo systemctl start crontab-ui.service