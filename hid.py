'''
Created on May 14, 2012

@author: indrio
'''

import win32api 
import win32con
import time

def mousePos(pos=(0,0)):
    win32api.SetCursorPos(pos)
    #print("Mouse @ {}".format(pos))
    
def leftClick(pos=(0,0), trigger=0):
    mousePos(pos)
    if trigger > 0.3:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1])
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])

