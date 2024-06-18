import canopen
import time
from driver import Driver

d = Driver(127, "od.eds", "can0")
node = d.getNode()



def initPDO():
    node.mnt.state = "PRE-OPERATIONAL"
    node.tpdo.read()
    node.tpdo[1].clear()
    node.tpdo[2].clear()
    node.tpdo[1].trans_type = 0xFF
    node.tpdo[2].trans_type = 0xFF
    node.tpdo[1].event_timer = 10
    node.tpdo[2].event_timer = 10
    node.tpdo[1].enabled = True
    node.tpdo[2].enabled = True
    node.tpdo[1].add_variable(0x6064) # Position actual value
    node.tpdo[1].add_variable(0x6044) # Actual velocity 
    node.tpdo[2].add_variable(0x20A0) # Additional position
    node.tpdo.save()
    node.nmt.state = "OPERATIONAL"


while True:
    print(node.sdo[0x6064].raw)
    print(node.sdo[0x6044].raw)
    print(node.sdo[0x20A0].raw)
    time.sleep(1)



