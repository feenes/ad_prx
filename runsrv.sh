#!/bin/bash

show_help() {
    cat << eot
starts the web server

usage $(basename $0) [-h|--help]

options:
    -h|--help       show this help text
eot
}

bd=$(cd $(dirname $0) ; pwd)
top_dir=$bd


## command line arg parsing
if which getopt > /dev/null ; then
    args=$(getopt -o h --long help -- "$@")
    if [ $? != 0 ] ; then
        echo invalid arguments use -h or --help for help 1>&2
        exit 1
    fi
    eval set -- "$args"
fi


while true ; do
    case "$1" in
        -h|--help) show_help ; exit 0 ;;
        --) shift ; break ;;
        *) break ;;
    esac
    shift
done

if [[ -f $top_dir/.envrc ]] ; then
    source $top_dir/.envrc
fi

cd "$bd"
exec sanic ad_prx.srv.app "$@"

