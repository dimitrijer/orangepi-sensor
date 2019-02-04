# OrangePi Zero Powered Temperature Sensor

I used [OrangePi Zero](http://www.orangepi.org/orangepizero/) to build a
low-cost temperature sensor.

## Hardware

* OrangePi Zero
* USB power adapter
* Case (optional)
* Class 10 4GB (or more) SD card
* OneWire DS18B20 temperature sensor
* USB-to-serial adapter (`lsusb` reports QinHeng Electronics HL-340 USB-Serial adapter)

## Kernel

Armbian has a really powerfull set of [build](https://github.com/armbian/build)
tools, and they also support OPZ out of the box. Vagrant build process is well
documented and keeps all the mess within builder VM.

I selected `next` kernel with default configuration, and I selected Debian
Stretch as image basis. In `config-default.conf`, I specified a separate 100M
FAT boot partition, which allows me to read SD card on Windows/Linux/Mac
machines (FAT partition needs to be the first primary partition on SD card for
Windows to read it).

I also have a custom script called `customize-image.sh`, which should be placed
in `userpatches` folder before building the image. This script is called in
chroot environment at the very end of build process. In it, I set up WiFi
network on startup by reading wireless network configuration - SSID and
passphrase -from a file called `wpa.txt` on boot partition. I also disable
NetworkManager and set up hostname according to `/boot/id.txt`.

At this point you can burn the image to the card and boot OPZ. You might want
to edit `/boot/wpa.txt` as OPZ will try to connect to WiFi on boot.

## System configuration

Now that I can access the sensor, I use Ansible to configure the system.

TODO users, services, software

## Metrics

Graphite is used as metrics aggregation engine.

I use Statsd on sensors to collect and periodically send metrics to Graphite.

## TODO

* Use [statsite](https://github.com/statsite/statsite) instead of Statsd for
  sending metrics - it is based on Statsd and actively maintained.
