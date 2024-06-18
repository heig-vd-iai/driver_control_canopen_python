import canopen
import time
import curses
from driver import Driver
import matplotlib.pyplot as plt


d = Driver(127, "od.eds", "can0")
node = d.getNode()

def initPDO():
    '''
    Init PDO communication
    '''
    node.nmt.state = "PRE-OPERATIONAL"
    node.tpdo.read()
    node.tpdo[1].clear()
    node.tpdo[2].clear()
    node.tpdo[1].trans_type = 0xFF
    node.tpdo[2].trans_type = 0xFF
    node.tpdo[1].event_timer = 1
    node.tpdo[2].event_timer = 1
    node.tpdo[1].enabled = True
    node.tpdo[2].enabled = True
    node.tpdo[1].add_variable(0x6064)  # Position actual value
    node.tpdo[1].add_variable(0x606C)  # Actual velocity
    node.tpdo[2].add_variable(0x20A0)  # Additional position
    node.tpdo.save()
    node.rpdo.read()
    node.rpdo[1].clear()
    node.rpdo[1].trans_type = 0xFF
    node.rpdo[1].add_variable(0x6071)
    node.rpdo[1].enabled = True
    node.rpdo.save()
    node.rpdo[1].start(0.001)
    node.nmt.state = "OPERATIONAL"


def getValue():
    '''
    Return PDO Value from driver
        Returns:
            tuple: (position, velocity, additional position)
    '''
    return node.pdo[0x6064].raw, node.pdo[0x606C].raw, node.pdo[0x20A0].raw


def init():
    initPDO()


def start():
    d.shutdown()
    d.switchOn()
    d.enableOperation()
    d.setMode(Driver.Mode.ProfileTorque)
    d.setTargetTorque(0)
    d.startOperation()


def main(screen):
    init()
    start()
    curses.curs_set(0)
    screen.addstr(0, 0, "===")
    screen.addstr(1, 0, f"Position: ")
    screen.addstr(2, 0, f"Velocity: ")
    screen.addstr(3, 0, f"Additional Position: ")
    screen.addstr(4, 0, f"===")
    i = 0
    try:
        while True:
            if i == 5000:
                node.rpdo[1][0x6071].raw = 100
            values = getValue()
            screen.addstr(1, 21, f"{values[0]:10}")
            screen.addstr(2, 21, f"{values[1]:10}")
            screen.addstr(3, 21, f"{values[2]:10}")
            screen.refresh()
            i += 1
            time.sleep(0.001)
    except KeyboardInterrupt:
        d.shutdown()


curses.wrapper(main)

