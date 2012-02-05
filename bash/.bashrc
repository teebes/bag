# --- often used aliases ---
alias ll='ls -la'
alias ac='source /code/ve/bin/activate'

# --- settings ---
export EDITOR="vi"

for f in ~/.bashrc.d/.bash* ;  do
    source $f; 
done

if [ -f ~/.bashrc.local ]; then
    source ~/.bashrc.local
fi

# --- colors ---
BLACK='\e[0;30m'
BLUE='\e[0;34m'
GREEN='\e[0;32m'
CYAN='\e[0;36m'
RED='\e[0;31m'
PURPLE='\e[0;35m'
BROWN='\e[0;33m'
LIGHTGRAY='\e[0;37m'
DARKGRAY='\e[1;30m'
LIGHTBLUE='\e[1;34m'
LIGHTGREEN='\e[1;32m'
LIGHTCYAN='\e[1;36m'
LIGHTRED='\e[1;31m'
LIGHTPURPLE='\e[1;35m'
YELLOW='\e[1;33m'
WHITE='\e[1;37m'
NC='\e[0m'              # No Color

# Meta-colors
BOLD='\e[1m'
BLINK='\e[5m'
REVERSE='\e[7m'

# --- git branch ---
git_branch() {
    if [ -e "$PWD/.git" ]; then
       git branch 2> /dev/null | grep '*' | awk '{if ($2) printf ("(%s) ", $2) }'
    fi
}

# --- ve warning ---
check_ve() {
    if [ -f ./bin/activate ] || [ -f ../bin/activate ] || [ -f ./ve/bin/activate ] || [ -f ../ve/bin/activate ]; then
        if [[ $VIRTUAL_ENV == "" ]] || [[ $PWD != *$VIRTUAL_ENV* ]] ; then
            #echo "You need to activate this ve"
            trash="nothing"
        fi
    fi
}

# --- set the prompt ---
export PS1="\[$LIGHTRED\]\$(check_ve)\n \[$LIGHTGREEN\]\$(git_branch)\[$YELLOW\]\u@\h: \w\n$ \[$NC\]"

case `uname` in
    IRIX64)
        SYS_BASE=sgi
        ;;
    SunOS)
        SYS_BASE=sun
        ;;
    Linux)
        SYS_BASE=linux
        ;;
    Darwin)
        SYS_BASE=mac
        ;;
    *)
        SYS_BASE=unknown
        ;;
esac

# --- mac ls coloring ---
if [ $SYS_BASE == "mac" ] ; then
    export CLICOLOR=1
    export LSCOLORS=ExFxCxDxBxegedabagacad
fi

if [ $SYS_BASE == "linux" ] ; then
    alias ls='ls --color=auto'
fi
