source "$ZDOTDIR/zsh-functions"
autoload -U colors && colors

# Basic auto/tab complete:
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}'
zmodload zsh/complist
compinit
_comp_options+=(globdots)		# Include hidden files.

# Other config files
zsh_add_file "zsh-variables"
zsh_add_file "zsh-prompt"
zsh_add_file "zsh-aliases"
zsh_add_file "zsh-vim-bindings"
zsh_add_file "zsh-export"

# Plugins
zsh_add_plugin "zsh-users/zsh-syntax-highlighting"
zsh_add_plugin "zsh-users/zsh-autosuggestions"
zsh_add_plugin "hlissner/zsh-autopair"

# Tools
[ -e /usr/share/fzf/key-bindings.zsh ] && source /usr/share/fzf/key-bindings.zsh
[ -e /usr/share/fzf/completion.zsh ] && source /usr/share/fzf/completion.zsh

# History in cache directory:
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.cache/zsh/history

