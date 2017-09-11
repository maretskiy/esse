test "${ENV_IS_SET_UP}" && return
export ENV_IS_SET_UP=1

export EDITOR=vim

alias ..='cd ..'
alias grep='grep --color=auto'
alias gr='grep -siIr --color=auto'
alias g='grep -siI --color=auto'
alias ls='ls --color=auto'
alias ll='ls -lhap --color=auto'
alias vi='vim -XNn'
alias d='df -hT'
alias e='emacs -nw'
alias f='free -m'
alias l=less
alias n='netstat -lnptu'
alias p='ps aux'
alias u='du -sh'

alias wget='wget -c -t 120 --no-check-certificate'
alias psgrep='ps aux | grep'
alias forget='ssh-keygen -f ${HOME}/.ssh/known_hosts= -R'

alias s='git status'
alias D='git diff'
alias B='git branch'
alias N='git branch --no-merged'
alias L='git log -3'
alias LL='git log -16 --oneline'
alias T='git log --oneline --decorate --graph'
alias S='git show'
alias SS='git show --stat'

+pyclean () {
    test -d "${1}"\
        && echo "removing *pyc files from ${1}"\
        && find "${1}" -type f -name \*.pyc -exec rm {} \;\
        && return
    echo "Usage: _pyclean <path/to/dir>">&2
}
alias _pyclean=+pyclean

if test $(id -u) -eq 0
then
    export PS1="\[\033[01;31m\]\u@\h:\[\033[01;34m\]\W\[\033[01;3\$(if test \${?} -eq 0; then echo 2; else echo 1; fi)m\]#\[\033[0m\] "
else
    export PS1="\[\033[01;33m\]\u@\h:\[\033[01;34m\]\W\[\033[01;3\$(if test \${?} -eq 0; then echo 2; else echo 1; fi)m\]$\[\033[0m\] "
fi

test -f ${HOME}/.bootstrap && . ${HOME}/.bootstrap
