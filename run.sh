#!/bin/bash

base_path=$PWD

interpreter="python3"

service="${base_path}/server.py"

set -e # Exit if any command fails

# Install python pip libraries
install_dependencies(){
    echo "Installing python libraries from pip3..."
    # apt-get install python3-pip
    pip3 install -r "${base_path}/requirements.txt"
    echo "Installed dependencies..."
}

start_process(){
    $interpreter $service &
}

stop_process(){
    echo "Killing process $(basename $service)"
    pkill -1 -f `basename $service` || true
}

if [[ "$1" == "stop" ]]; then
    stop_process
    echo "Process killed..."
    exit 0
fi

if [[ "$1" == "start" ]]; then
    echo "Process starting..."
    start_process
    exit 0
fi

if [[ "$1" == "install" ]]; then
    echo "Installation started..."
    install_dependencies
    exit 0
fi

echo "Command not found"