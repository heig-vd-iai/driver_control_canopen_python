# Getting Started with Raspberry pi
- Flash RaspbianOS 64Bits with raspberry pi imager
- `sudo apt update && sudo apt upgrade`

# Configure can
Add 
```bash
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
```
to `/boot/config.txt`

> [!NOTE]
> oscillator is the frequency of the crystal connected to the MCP2515. The default value is 12MHz. If you are using a other frequency, you must change this value.



reboot raspberry pi
```bash
sudo reboot
```
After rebooting, run the command to see if the initialization was successful:
```bash
dmesg | grep -i '\(can\|spi\)'
```
Add this line to `/etc/rc.local` before `exit 0`:
```bash
sudo ip link set can0 up type can bitrate 500000
sudo ifconfig can0 txqueuelen 65536
```

> [!NOTE]
> The bitrate is 500kbps for the can transmission. If you want to change the bitrate, you must change this value.


# Driver Library
The driver.py library allows interfacing with the driver of the ServoPress2 board.

## Connection
Exemple for connect to device with id 1, using the object dictionary file "od.eds" and the can interface "can0":
```python
from driver import Driver
d = Driver(1, "od.eds", "can0")
```


