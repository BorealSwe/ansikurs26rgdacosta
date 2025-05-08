#!/bin/bash

read -p "Which host are you targetting? " MY_HOST
read -p "Which software package are you managing? " MY_PACKAGE
echo -e "Now choose from the following:\n"
echo -e "installed - installs software\n"
echo -e "removed - removes software\n"
echo -e "latest - upgrades software\n"
read MY_STATE 

ansible-navigator run manage_software.yml -e my_host=$MY_HOST -e my_package=$MY_PACKAGE -e my_state=$MY_STATE
