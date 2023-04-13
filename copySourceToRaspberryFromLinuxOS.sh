#***************************************************
# This script copy all needed sources from a Linux 
# system to the rasperry.


LinuxUsername=pi

sudo rm -rf $LinuxUsername@$1:/home/$LinuxUsername/*
#sudo scp -rv ~/dev/mbus_modbus_simulator/*.* $LinuxUsername@$1:/home/$LinuxUsername
sudo scp -rv *.* $LinuxUsername@$1:/home/$LinuxUsername


# DIR="~/dev/mbus_modbus_simulator/"
# if [ -d "$DIR" ]; then
#   ### Take action if $DIR exists ###
#   echo "Copy files from ${DIR} to the system $LinuxUsername"
#   sudo scp -rv ${DIR}*.* $LinuxUsername@$1:/home/$LinuxUsername
# else
#   ###  Control will jump here if $DIR does NOT exists ###
#   echo "Error: ${DIR} not found. Can not continue."
#   exit 1
# fi


