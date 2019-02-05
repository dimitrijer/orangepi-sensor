# OrangePi Zero Powered Temperature Sensor

I used [OrangePi Zero](http://www.orangepi.org/orangepizero/) to build a low-cost, self-updating temperature sensor. It uses Wifi for connectivity.
Connection parameters are stored as plaintext files on FAT32 /boot partition.

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
Stretch as base image. In `config-default.conf`, I specified a separate 100M
FAT boot partition, which allows me to read SD card on Windows/Linux/Mac
machines (FAT partition needs to be the first primary partition on SD card for
Windows to read it).

I also have a custom script called `customize-image.sh`, which should be placed
in `userpatches` folder before building the image. This script is called in
chroot environment at the very end of build process. In it, I set up WiFi
network on startup by reading wireless network configuration - SSID and
passphrase - from a file called `wpa.txt` on boot partition. I also disable
NetworkManager, set up hostname according to `/boot/id.txt` and disable
first-time password change for root user and login user creation (Ansible will
manage that).

At this point you can burn the image to the card and boot OPZ. You might want
to edit `/boot/wpa.txt` as OPZ will try to connect to WiFi on boot.

## System configuration

Now that I can ssh to the box, I can use Ansible to provision the system.

You need to install additional roles from Galaxy with:
```bash
ansible-galaxy install -r requirements.yml
```

Three roles are used:
* [nickjj/ansible-docker](https://github.com/nickjj/ansible-docker) role is
   used to install and configure Docker
* `users` role is used to create login user and setup authorized keys and sudo
   (default root password is changed after provisioning)
* `services` role starts services via `docker-compose`

Invoke `ansible-playbook` to start provisioning:
```bash
ansible-playbook --vault-id @prompt -i inventories/hosts.ini playbook.yml
```

Note that you will need to have fingerprint of the box in your
`~/.ssh/known_hosts` file in order for Ansible to use default root password
(stored in group vars). You can fingerprint the box with:

```bash
ssh-keyscan -H <box_ip> ~/.ssh/known_hosts
```

## Services

I use three containers, managed by `docker-compose.yml`.
* Statsd container that is used to aggregate metrics locally and send metrics
  to Graphite server
* Python script that runs in a container, reads temperature and sends readings
  to Statsd via UDP
* [Watchtower](https://github.com/v2tec/watchtower) container that monitors
  Docker repository for new versions of images of running containers, downloads
  them and restarts running container instances (including itself)

## Metrics

Graphite is used as metrics aggregation engine, and Grafana is used to display
them in a nice dashboard.

## Images

Front (single USB port and Ethernet port can be seen)

![Front](/images/opz1.jpg)

Rear (microSD slot on the bottom and mini USB for power)

![Rear](/images/opz2.jpg)

Top

![Top](/images/opz3.jpg)

## TODO

* Add sensor picture
* Add Grafana screenshot
* Use [statsite](https://github.com/statsite/statsite) instead of Statsd for
  sending metrics - it is based on Statsd and actively maintained
* Use OpenVPN to connect sensor boxes to home VPN and be able to SSH to them,
  no matter where they are deployed
