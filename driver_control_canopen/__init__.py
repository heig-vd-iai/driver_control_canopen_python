from enum import Enum
import canopen
import struct
import time
import yaml
from voluptuous import MultipleInvalid
# from canopen_stack.canopen_generator.schema import profile_schema, config_schema

shutdownMask = 0b10000111
shutdownCommand = 0b00000110
switchOnMask = 0b1001111
switchOnCommand = 0b00000111
disableVoltageMask = 0b10000010
disableVoltageCommand = 0b00000000
quickStopMask = 0b10000110
quickStopCommand = 0b00000010
disableOperationMask = 0b10001111
disableOperationCommand = 0b0000111
enableOperationMask = 0b10001111
enableOperationCommand = 0b00001111
faultResetMask = 0b10000000
faultResetCommand = 0b10000000
startOperationMask = 0b00010000
startOperationCommand = 0b00010000
changeSetImmediatelyMask = 0b00100000
changeSetImmediatelyEnable = 0b00100000
absolutePositionMask = 0b01000000
absolutePositionEnable = 0b01000000
haltMask = 0b0000000100000000
haltCommand = 0b0000000100000000
changeOnSetPointMask = 0b0000001000000000
changeOnSetPointEnable = 0b0000001000000000
noneCommand = 0b0000000000000000


def startDriver():
    driver = Driver(1, "meccad.eds", 'can0')
    time.sleep(2)
    driver.shutdown()
    time.sleep(1)
    driver.switchOn()
    time.sleep(1)
    driver.enableOperation()
    time.sleep(1)
    return driver


class Driver:
    def __init__(self, nodeNumber, od, interface):
        node = nodeNumber
        self.od = od
        self.interface = interface
        try:
            self.node = canopen.Node(nodeNumber, od)
            network = canopen.Network()
            network.add_node(self.node)
            network.connect(channel=interface, bustype='socketcan')
            self.node.sdo.RESPONSE_TIMEOUT = 3
            print(f"Connected to {interface}")
        except Exception as e:
            print(e)

    class Mode(Enum):
        ProfilePosition = 1
        ProfileTorque = 4
        Homing = 6

    class SaveParameters(Enum):
        All = 1
        Communication = 2
        Application = 3
        Manufacturer = 4

    class Subobject:
        def __init__(self, driver, index):
            self.driver = driver
            self.index = index

        def __getitem__(self, subindex):
            try:
                return self.driver.node.sdo[self.index].raw
            except:
                return self.driver.node.sdo[self.index][subindex].raw

        def __setitem__(self, subindex, value):
            try:
                self.driver.node.sdo[self.index][subindex].raw = value
            except:
                self.driver.node.sdo[self.index].raw = value

    def __getitem__(self, index):
        return self.Subobject(self, index)

    def configure(self, settingFile, configFile):
        with open(settingFile, "r") as f:
            data = yaml.safe_load(f)
        with open(configFile, "r") as f:
            config = config_schema(yaml.safe_load(f))

        for i, module in data.items():
            for index, object in module.items():
                ind = 0
                for i, od_index in config["objectDictionary"].items():
                    if od_index["alias"] == index:
                        ind = i
                if ind == 0:
                    print(f"❌ {index} not found in object dictionary")
                    continue
                for subindex, data in object.items():
                    print(
                        f"❕ write {data} to {hex(ind)}.{hex(subindex)}")
                    self[ind][subindex] = data
                    time.sleep(0.02)
        self.node.sdo[0x1010][1].phys = 0x65766173
        print("\n\n✅ save parameter in drive")

    
    def getNode(self):
        return self.node

    def reset(self):
        self.node.nmt.state = 'RESET'

    def shutdown(self):
        self.node.sdo[0x6040].phys = 0x06

    def switchOn(self):
        self.node.sdo[0x6040].phys = 0x07

    def disableVoltage(self):
        self.node.sdo[0x6040].phys = 0x00

    def quickStop(self):
        self.node.sdo[0x6040].phys = 0x02

    def disableOperation(self):
        self.node.sdo[0x6040].phys = 0x07

    def enableOperation(self):
        self.node.sdo[0x6040].phys = 0x0F

    def faultReset(self):
        self.node.sdo[0x6040].phys = 0x80

    def setMode(self, mode):
        if type(mode) == self.Mode:
            self.node.sdo[0x6060].phys = mode.value
            return
        self.node.sdo[0x6060].phys = mode

    def startOperation(self):
        self.node.sdo[0x6040].raw = (
            self.node.sdo[0x6040].raw & ~startOperationMask) | startOperationCommand
        self.node.sdo[0x6040].raw = (
            self.node.sdo[0x6040].raw & ~startOperationMask) | noneCommand

    def getStatusWord(self):
        return self.node.sdo[0x6041].phys

    def getOperationDisplay(self):
        return self.node.sdo[0x6061].phys

    def getDemandPosition(self):
        return self.node.sdo[0x6062].phys

    def getActualPosition(self):
        return self.node.sdo[0x6064].raw

    def getDemandVelocity(self):
        return self.node.sdo[0x606B].phys

    def getActualVelocity(self):
        return self.node.sdo[0x606C].phys

    def setTargetTorque(self, torque: int):
        self.node.sdo[0x6071].phys = torque

    def getTargetTorque(self):
        return self.node.sdo[0x6071].phys

    def getActualTorque(self):
        return self.node.sdo[0x6077].phys

    def getActualCurrent(self):
        return self.node.sdo[0x6078].phys

    def getTargetPosition(self):
        return self.node.sdo[0x607A].phys

    def setTargetPosition(self, position: int):
        self.node.sdo[0x607A].phys = position

    def getProfileVelocity(self):
        return self.node.sdo[0x6081].phys

    def setProfileVelocity(self, velocity: int):
        self.node.sdo[0x6081].phys = velocity

    def getProfileAcceleration(self):
        return self.node.sdo[0x6083].phys

    def setProfileAcceleration(self, acceleration: int):
        self.node.sdo[0x6083].phys = acceleration

    def getProfileDeceleration(self):
        return self.node.sdo[0x6084].phys

    def setProfileDeceleration(self, deceleration):
        self.node.sdo[0x6084].phys = deceleration

    def getTorqueSlope(self):
        return self.node.sdo[0x6087].phys

    def setTorqueSlope(self, value):
        self.node.sdo[0x6087].phys = value

    def saveParameters(self, parameter):
        if type(parameter) == self.SaveParameters:
            self.node.sdo[0x1010][parameter.value].phys = 0x65766173
            return
        self.node.sdo[0x1010][parameter].phys = 0x65766173

    def resetDefaultParameters(self, parameter):
        if type(parameter) == self.SaveParameters:
            self.node.sdo[0x1011][parameter.value].phys = 0x64616F6C
            return
        self.node.sdo[0x1011][parameter].phys = 0x64616F6C

    def getTrace(self, index):
        data = []
        data = list(struct.unpack("f" * 200, self.node.sdo[0x5000+index].raw))
        time.sleep(0.01)
        while self.node.sdo[0x2855][1+index].raw > 0:
            data += list(struct.unpack("f" * 200,
                         self.node.sdo[0x5000+index].raw))
            time.sleep(0.01)
        return data

    def _setPositionSwitch(self, state):
        self.node.sdo[0x2700][1].phys = state

    def _setVelocitySwitch(self, state):
        self.node.sdo[0x2700][2].phys = state

    def _setCurrentSwitch(self, state):
        self.node.sdo[0x2700][3].phys = state
