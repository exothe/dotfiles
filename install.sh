source ~/.config/scripts/install_package.sh

install_package zsh
printf "export ZDOTDIR=~/.config/zsh\nsource ~/.config/zsh/.zshrc" > ~/.zshrc
chsh -s /usr/bin/zsh

install_package tmux
echo source ~/.config/tmux/.tmux.conf > ~/.tmux.conf
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

git clone https://github.com/MissSis/neovim-config.git ~/.config/nvim/
install_package neovim
git clone --depth 1 https://github.com/wbthomason/packer.nvim ~/.local/share/nvim/site/pack/packer/start/packer.nvim

zsh
