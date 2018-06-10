#!/bin/sh


echo '--------------------------------------------'
echo 'Install ZSH and the GRML-ZSH configuration'
sudo apt-get -qq -y install zsh >> /dev/null
sudo wget -O /etc/zsh/zshrc  https://raw.githubusercontent.com/grml/grml-etc-core/master/etc/zsh/zshrc 
sudo chsh -s /usr/bin/zsh pi
sudo chsh -s /usr/bin/zsh
sudo -u pi touch /home/pi/.zshrc

echo '--------------------------------------------'
echo 'Install VIM'
sudo apt-get -qq -y install vim >> /dev/null

echo '--------------------------------------------'
