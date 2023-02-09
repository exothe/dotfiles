source ~/.config/scripts/install_package.sh

install_package zsh
printf "export ZDOTDIR=~/.config/zsh\nsource ~/.config/zsh/.zshrc" > ~/.zshrc
chsh -s /usr/bin/zsh

install_package tmux
echo source ~/.config/tmux/.tmux.conf > ~/.tmux.conf

zsh
