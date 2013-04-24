import sys, time, threading
import PySixense
from hid import *

class HydraData(object):
    def __init__(self, controllers):
        """Initialize what controllers do you want to get motion from"""
        self.controllers = controllers
        self.hand = {}
        self.counter = 0
    
    def getData(self):
        while True:
            self.counter +=1
            for ctrl in self.controllers:
                success, data = PySixense.GetNewestData(ctrl)
                if success == PySixense.Constants.Failure:
                    print("Could not get data of controller {}!".format(ctrl))
                else:
                    self.hand[ctrl] = data

    @property
    def lefthand(self):
        return self.hand[0]

    @property
    def righthand(self):
        return self.hand[1]

class HydraManager(object):
    def __init__(self, controllers=[0,1]):
        # init
        assert(PySixense.Init() == PySixense.Constants.Success)
        time.sleep(1) # sleep until initialization if done
        self.hydra = HydraData(controllers)
        self.recordData()

    def recordData(self):
        td = threading.Thread(target=self.hydra.getData)
        td.start()

    def samplingRate(self):
        sc = self.hydra.counter
        time.sleep(1)
        total = self.hydra.counter - sc
        print("PySixense DataRate: {} {}, {} {}, {} {}".format(total, "Samples/Sec"\
                , total/1000, "Khz", total/1000000, "Mhz"))

class HydraMapping(object):
    def __init__(self, HM, mapping={'pos':'mouse', 'joystick':'wasd'}, sensitivity=1):
        self.HM = HM # HydraManager
        self.mapping = mapping
        self.sensitivity = sensitivity
        self.startMotion()

    def startMotion(self):
        """Initializes threads for each mapping event"""
        for h,k in self.mapping.items():
            self.threads = []
            if h == 'pos' and k == 'mouse':
                target = self.performClick
            elif h == 'joystick' and k == 'wasd':
                target = self.performMove
            h_thread = threading.Thread(target=target)
            self.threads.append(h_thread)
            h_thread.start()

    def performMove(self):
        """performs x,y movements and based on lefthand hydra joystick"""
        while 1:
            x = int(self.HM.hydra.lefthand.joystick_x)
            y = int(self.HM.hydra.lefthand.joystick_y)
            trigger = self.HM.hydra.lefthand.trigger
            if x < 0:
                keyPress('A')
            if x > 0:
                keyPress('D')
            if y > 0:
                keyPress('W')
            if y < 0:
                keyPress('S')
    def performClick(self):
        """performs x,y movements and clicks based on hydra trigger"""
        while 1:
            trigger = self.HM.hydra.righthand.trigger
            if trigger > 0:
                while 1:
                    self.x = int(640 + self.HM.hydra.righthand.pos[0]/self.sensitivity)
                    self.y = int(400 - self.HM.hydra.righthand.pos[1]/self.sensitivity)
                    trigger = self.HM.hydra.righthand.trigger
                    button = self.HM.hydra.righthand.buttons
                    leftClick((self.x, self.y), button)
                    if trigger > 0.5: # Toggle xy righthand motion based on trigger
                       break
if __name__ == '__main__':
    HMan = HydraManager() # Initialize RazerHydra threads
    HMapping = HydraMapping(HMan, sensitivity=4)

    while True:
        HMan.samplingRate()
        #x,y,z = HMan.hydra.righthand.pos[0], HMan.hydra.righthand.pos[1], HMan.hydra.righthand.pos[2] 
        #print("{:.2f} {:.2f} {:.2f}".format(x,y,z))
        #print(win32api.GetCursorPos())
        #print("{},{}".format(HMan.hydra.lefthand.joystick_x,HMan.hydra.lefthand.joystick_y))
        #print("Button: {} Trigger: {}".format(HMan.hydra.lefthand.buttons, HMan.hydra.lefthand.trigger))
        #print(PySixense.GetNewestData(0).pos)
        time.sleep(1)
