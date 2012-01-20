#! /usr/bin/bash

dirs=(git bash vim screen)

for dir in ${dirs[@]}
do
    if [ $dir = "git" ] ; then
        if [ -e "~/.gitconfig" ] ; then
            echo "there is a gitconfig!" ;
        fi
    elif [ $dir = "bash" ] ; then
        echo "this is" $dir ;
    fi
done
