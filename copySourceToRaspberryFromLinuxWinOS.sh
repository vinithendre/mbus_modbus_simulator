#***************************************************
# This script copy all needed sources from a windows 
# system to the rasperry.


LinuxUsername=ubuntu

rm -rf $LinuxUsername@$1:/home/$LinuxUsername/*
scp -rv ./* $LinuxUsername@$1:/home/$LinuxUsername