#!/bin/bash

# arguments: $RELEASE $LINUXFAMILY $BOARD $BUILD_DESKTOP
#
# This is the image customization script

# NOTE: It is copied to /tmp directory inside the image
# and executed there inside chroot environment
# so don't reference any files that are not already installed

# NOTE: If you want to transfer files between chroot and host
# userpatches/overlay directory on host is bind-mounted to /tmp/overlay in chroot

RELEASE=$1
LINUXFAMILY=$2
BOARD=$3
BUILD_DESKTOP=$4

Main() {
	case $RELEASE in
		jessie)
			# your code here
			;;
		xenial)
			# your code here
			;;
		stretch)
			# your code here
            SetupSensor
			;;
	esac
} # Main

SetupSensor() {
    # Setup stuff in /boot
    echo "alpha" > /boot/id.txt
    echo "network={
 ssid=\"Foundation\"
 psk=\"mijedobiogrip\"
 #key_mgmt=NONE
}" > /boot/wpa.txt

    # Prepare interfaces
    echo "allow-hotplug eth0
no-auto-down eth0
iface eth0 inet dhcp" > /etc/network/interfaces.d/eth0
    echo "auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
    wpa-conf /boot/wpa.txt" > /etc/network/interfaces.d/wlan0
    echo "auto lo
iface lo inet loopback" > /etc/network/interfaces.d/lo
    echo "source /etc/network/interfaces.d/*" > /etc/network/interfaces

    # We don't need NM
    systemctl disable NetworkManager.service

    # Disable interactive first login
    rm -f /root/.not_logged_in_yet
    echo -e "1234\n1234" | (passwd root)
}

Main "$@"

