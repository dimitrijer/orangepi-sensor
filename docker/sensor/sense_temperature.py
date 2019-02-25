#!/usr/bin/env python3

import subprocess
import time

from digitemp.master import UART_Adapter
from digitemp.device import AddressableDevice, DS18B20
from timeit import default_timer as timer
from statsd import StatsClient

CYCLE_TIME_SECONDS = 20
MIN_SLEEP_INTERVAL = 1

def get_roms():
    try:
        start = timer()
        roms = AddressableDevice(bus).get_connected_ROMs()
        elapsed = int(1000 * (timer() - start))
        stats.timing('getroms.%s.timed' % sensor_id, elapsed)
        stats.gauge('getroms.%s.devices' % sensor_id, len(roms))
        return roms
    except:
        stats.incr('getroms.%s.errors' % sensor_id)
        return []
    finally:
        stats.incr('getroms.%s.total' % sensor_id)

def read_temperature(rom):
    try:
        start = timer()
        device = DS18B20(bus, rom=rom)
        temperature = int(device.get_temperature() * 1000)
        print(str(rom) + '=' + str(temperature))
        stats.gauge('readroms.%s.temperature' % rom, temperature)
        elapsed = int(1000 * (timer() - start))
        stats.timing('readroms.%s.timed' % rom, elapsed)
    except:
        stats.incr('readroms.%s.errors' % rom)
    finally:
        stats.incr('readroms.%s.total' % rom)

def led_toggle(value):
    p1 = subprocess.Popen(["echo", str(value)], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["tee", "/sys/class/leds/orangepi:red:status/brightness"], stdin=p1.stdout)
    p2.communicate()

def read_cpu_temperature():
    try:
        region0_temperature = subprocess.check_output(["cat", "/etc/armbianmonitor/datasources/soctemp"])
        return float(region0_temperature)
    except:
        return float(-1)

if __name__ == '__main__':
    start = timer()

    bus = UART_Adapter('/dev/ttyUSB0')
    stats = StatsClient('statsd', 8125, 'readtemp')
    try:
        with open('/boot/id.txt', 'r') as f:
            sensor_id = f.readline().strip()
    except:
        sensor_id = 'unknown'

    stats.gauge('online.%s' % sensor_id, 1)
    led_toggle(1)
    for rom in get_roms():
        read_temperature(rom)
    led_toggle(0)

    elapsed_time = timer() - start
    stats.timing('runtime.%s.elapsed' % sensor_id, int(1000 * elapsed_time))

    stats.gauge('system.%s.cpu.temperature' % sensor_id, read_cpu_temperature())

    sleep_interval = CYCLE_TIME_SECONDS - elapsed_time
    if sleep_interval > MIN_SLEEP_INTERVAL:
        # Sleep some time before docker restarts the container
        print('Sleeping for {0:.3f}s...'.format(sleep_interval))
        time.sleep(sleep_interval)

    elapsed_total = timer() - start
    stats.timing('runtime.%s.total_elapsed' % sensor_id, int(1000 * elapsed_total))
