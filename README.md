# OrangePi Zero Powered Temperature Sensor

I used [OrangePi Zero](http://www.orangepi.org/orangepizero/) to build a
low-cost temperature sensor.

## Hardware

1 x OrangePi Zero
1 x USB power adapter
1 x case (optional)
1 x Class 10 4GB (or more) SD card
1 x OneWire DS18B20 temperature sensor
1 x USB-to-serial adapter (`lsusb` reports QinHeng Electronics HL-340 USB-Serial adapter)

## Kernel

Armbian has a really powerfull set of [build](https://github.com/armbian/build)
tools, and they also support OPZ out of the box. Vagrant build process is well
documented and keeps all the mess within builder VM.

I selected `next` kernel with default configuration. In `config-default.conf`,
I specified a separate 100M FAT boot partition, which allows me to read SD card
on Windows/Linux/Mac machines (FAT partition needs to be the first primary
partition on SD card for Windows to read it).

I also have a custom script called `customize-image.sh`, which should be placed
in `userpatches` folder before building the image. This script is called in
chroot environment at the very end of build process. In it, I set up WiFi
network on startup by reading wireless network configuration - SSID and
passphrase -from a file called `wpa.txt` on boot partition. I also disable
NetworkManager and set up hostname according to `/boot/id.txt`.
