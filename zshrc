export EDITOR=vim
bindkey -e

HISTFILE=${HOME}/.zsh_history
HISTSIZE=2000
SAVEHIST=2000
setopt hist_ignore_dups hist_ignore_space inc_append_history

autoload -Uz compinit && compinit -i

alias ..='cd ..'
alias grep='grep --color=auto'
alias gr='grep -siIr --color=auto'
alias g='grep -siI --color=auto'
alias ls='ls -G'
alias ll='ls -lhapG'
alias vi='vim -XNn'
alias d='df -h'
alias e='vim -XNn'
alias f='vm_stat'
alias l=less
alias n='lsof -iTCP -sTCP:LISTEN -P -n'
alias p='ps aux'
alias u='du -sh'

alias wget='wget -c -t 120 --no-check-certificate'
alias psgrep='ps auxww | grep'
alias forget='ssh-keygen -f ${HOME}/.ssh/known_hosts -R'

alias s='git status'
alias D='git diff'
alias B='git branch'
alias N='git branch --no-merged'
alias L='git log -3'
alias LL='git log -16 --oneline'
alias T='git log --oneline --decorate --graph'
alias S='git show'
alias SS='git show --stat'

function +pyclean {
    test -d "${1}"\
        && echo "removing __pycache__ dirs from ${1}"\
        && find "${1}" -type d -name __pycache__ -prune -exec rm -rf {} +\
        && return
    echo "Usage: _pyclean <path/to/dir>">&2
}
alias _pyclean=+pyclean

PROMPT='%B%(!.%F{red}.%F{yellow})%n@%m:%F{blue}%1~%(?.%F{green}.%F{red})%(!.#.$)%f%b '

if test -f "${HOME}/.zshsetup"
then
    . "${HOME}/.zshsetup"
fi
