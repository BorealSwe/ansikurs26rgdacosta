#!/bin/bash
my_user=john
my_uid=10000
my_shell=/bin/bash

if [ "$(getent passwd ${my_user} | awk -F: '{print $1}')" = "${my_user}" ]
        then
           echo "The user ${my_user} exists"
	   exit
        else
           useradd -u ${my_uid} ${my_user}
           echo $?
fi

if [ "$(getent passwd ${my_user} | awk -F: '{print $3}')" -ne "${my_uid}" ]
        then
            usermod -u ${my_uid} ${my_user}
        else
           echo "The user ${my_user} exists with ${my_uid}"
fi


