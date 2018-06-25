#!/bin/sh


echo '--------------------------------------------'
echo 'Install ZSH and the GRML-ZSH configuration'
sudo apt-get -qq -y install zsh >> /dev/null
sudo wget -O /etc/zsh/zshrc https://raw.githubusercontent.com/grml/grml-etc-core/master/etc/zsh/zshrc 
sudo chsh -s /usr/bin/zsh pi
sudo chsh -s /usr/bin/zsh
sudo -u pi touch /home/pi/.zshrc

echo '--------------------------------------------'
echo 'Install VIM'
sudo apt-get -qq -y install vim >> /dev/null
wget -O /etc/vim/vimrc http://git.grml.org/f/grml-etc-core/etc/vim/vimrc
echo 'set tabstop=2' >> /etc/vim/vimrc
echo 'set shiftwidth=2' >> /etc/vim/vimrc
echo 'set expandtab' >> /etc/vim/vimrc
echo 'set paste' >> /etc/vim/vimrc

echo '--------------------------------------------'
echo 'Install screen'
sudo apt-get -qq -y install screen >> /dev/null
wget -O /etc/screenrc http://git.grml.org/f/grml-etc-core/etc/grml/screenrc_generic

echo '--------------------------------------------'
echo 'Install nmon'
sudo apt-get -qq -y install nmon >> /dev/null

echo '--------------------------------------------'
echo 'Install iftop'
sudo apt-get -qq -y install iftop >> /dev/null

echo '--------------------------------------------'
echo 'Install htop'
sudo apt-get -qq -y install htop >> /dev/null

echo '--------------------------------------------'
