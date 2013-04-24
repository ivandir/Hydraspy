'''
Created on May 14, 2012

@author: indrio
'''
import PySixense
import win32api 
import win32con
import time

button_was_pressed = False

def mousePos(pos=(0,0)):
    win32api.SetCursorPos(pos)
    #print("Mouse @ {}".format(pos))
    
def leftClick(pos=(0,0), button=0):
    global button_was_pressed
    mousePos(pos)
    if button:
       button_was_pressed = True
       win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1])
    elif not button and button_was_pressed:
       button_was_pressed = False
       win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])

def keyPress(key):
        win32api.keybd_event(ord(key), 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_KEYUP, 0)


if __name__ == "__main__":
        assert(PySixense.Init() == PySixense.Constants.Success)
        while 1:
            success, data = PySixense.GetNewestData(1)
            trigger = data.trigger
            if trigger > 0:
                while 1:
                    success, data = PySixense.GetNewestData(1)
                    x = int(960 + data.pos[0]/4)
                    y = int(540 - data.pos[1]/4)
                    trigger = data.trigger
                    button = data.buttons
                    leftClick((x, y), button)
                    if trigger > 0.5: # Toggle xy righthand motion based on trigger
                       break
