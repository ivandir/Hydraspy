import sys, time, threading, copy, gc
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


    def recordlefthand(self):
        while 1:
            success, data = PySixense.GetNewestData(0)
            if success == PySixense.Constants.Failure:
                print("Could not get data of controller {}!".format(0))
            else:
                self.hand[0] = data

    def recordrighthand(self):
        while 1:
            success, data = PySixense.GetNewestData(1)
            if success == PySixense.Constants.Failure:
                print("Could not get data of controller {}!".format(1))
            else:
                self.hand[1] = data

class HydraManager(object):
    def __init__(self, controllers=[0,1]):
        # init
        assert(PySixense.Init() == PySixense.Constants.Success)
        time.sleep(1) # sleep until initialization if done
        self.hydra = HydraData(controllers)
        self.recordData()
        #self.startThreads()

    def startThreads(self):
        threads = []
        tleft = threading.Thread(target=self.hydra.recordlefthand)
        tright = threading.Thread(target=self.hydra.recordrighthand)
        threads.append(tleft)
        threads.append(tright)
        tleft.start()
        tright.start()

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
    def __init__(self, HM, mapping={'pos':'mouse', 'joystick':'wasd'}):
        self.HM = HM # HydraManager
        self.mapping = mapping
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
        """performs x,y movements and based on righthand hydra joystick"""
        while 1:
            x = int(self.HM.hydra.righthand.joystick_x)
            y = int(self.HM.hydra.righthand.joystick_y)
            trigger = self.HM.hydra.righthand.trigger
            if x < 0:
                keyPress('a')
            elif x > 0:
                pass
                # (TODO) press d

            if y > 0:
                pass
                # (TODO) press w
            elif y < 0:
                pass
                # (TODO) press s
    def performClick(self):
        """performs x,y movements and clicks based on hydra trigger"""
        while 1:
            x = int(self.HM.hydra.lefthand.pos[0]+800)
            y = int(self.HM.hydra.lefthand.pos[1]*-1.5+450)
            trigger = self.HM.hydra.lefthand.trigger
            if trigger > 0.1:
                leftClick((x, y), trigger)
            else:
                mousePos((x,y))

if __name__ == '__main__':
    gc.disable()
    HMan = HydraManager() # Initialize RazerHydra threads
    HMapping = HydraMapping(HMan)

    while True:
        #HMan.samplingRate()
        #x,y,z = HMan.hydra.lefthand.pos[0], HMan.hydra.lefthand.pos[1], HMan.hydra.lefthand.pos[2] 
        #print("{:.2f} {:.2f} {:.2f}".format(x,y,z))
        #print("{},{}".format(HMan.hydra.lefthand.joystick_x,HMan.hydra.lefthand.joystick_y))
        #print("Button: {} Trigger: {}".format(HMan.hydra.lefthand.buttons, HMan.hydra.lefthand.trigger))
        #print(PySixense.GetNewestData(0).pos)
        pass

