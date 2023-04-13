#This script is required if the Raspberry PI should be assigned a fixed IP

# $1 --> current IP from the raspberry
# $2 --> new static IP

fileName="50-cloud-init.yaml"
destinationPath="/etc/netplan/"

sudo chmod 777 $destinationPath


rm -f -- $fileName

echo "network:" >> $fileName
echo "  version: 2" >> $fileName
echo "  renderer: networkd" >> $fileName
echo "  ethernets:" >> $fileName
echo "    eth0:" >> $fileName
echo "     dhcp4: no" >> $fileName
echo "     addresses: [$2/24]" >> $fileName
echo "     gateway4: 139.16.87.1" >> $fileName
echo "     nameservers:" >> $fileName
echo "       addresses: [129.103.96.71,129.103.99.237,129.103.95.73,129.103.95.71]" >> $fileName




#mv ubuntu@$1 sudo systemctl status startSimulator.service 
#mmv ubuntu@$1:/etc/netplan/$fileName  ubuntu@$1:/etc/netplan/$fileName.bak
#msudo scp $fileName ubuntu@$1:/etc/netplan/$fileName

sudo chmod 644 $destinationPath