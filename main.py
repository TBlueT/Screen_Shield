# -*- coding: utf-8 -*-
import sys
import os, time
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDialog, QSplashScreen
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6 import uic

from win32api import GetCursorPos, keybd_event, GetKeyState, EnumDisplayMonitors
import win32con
import keyboard
from PaintLabel import *

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        monitor = EnumDisplayMonitors()
        monitorMap = list()
        self.monitors = []
        for info in monitor:
            self.monitors.append([info[2][0], info[2][1], info[2][2], info[2][3]])

        layout = QVBoxLayout()

        self.view = PaintLabel(self)
        self.view.resize(40,40)
        layout.addWidget(self.view)

        self.setLayout(layout)

        self.mouseMove = moveMus()
        self.mouseMove.Set_MovePoint.connect(self.Set_MovePoint)
        self.mouseMove.Set_WinShield.connect(self.Set_WinShield)
        self.mouseMove.Set_WinShield_Close.connect(self.Set_WinShield_Close)

        self.mouseMove.start()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_Disabled, True)
        self.resize(40, 40)
        self.M = False

        self.WinShieldName = []

    @pyqtSlot(int, int, int)
    def Set_MovePoint(self, x, y, d):
        self.move(x, y)

    @pyqtSlot()
    def Set_WinShield(self):
        if not self.M:
            for i in self.monitors:
                x = i[2] - i[0]
                y = i[3] - i[1]
                print("asd",i[0], i[1], x,y)
                setattr(self, F"Shield_{i}",Shield(i[0], i[1], x, y))
                self.WinShieldName.append(F"Shield_{i}")
                print(self.WinShieldName)
            self.M = True

    @pyqtSlot()
    def Set_WinShield_Close(self):
        for i in self.WinShieldName:
            getattr(self, i).close()
        self.WinShieldName = []
        self.M = False


class Shield(QDialog):
    def __init__(self, x, y, w, h):
        super(Shield, self).__init__()
        print(x,y,w,h)
        self.move(x,y)
        self.resize(w, h)
        self.setStyleSheet("background:rgb(0,0,0)")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showFullScreen()


        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        # self.setAttribute(Qt.WidgetAttribute.WA_Disabled, False)

        layout = QVBoxLayout()

        self.view = PaintLabel(self, h/4, w/2, h/2)
        layout.addWidget(self.view)

        self.setLayout(layout)

class moveMus(QThread):
    Set_MovePoint = pyqtSignal(int, int, int)
    Set_WinShield = pyqtSignal()
    Set_WinShield_Close = pyqtSignal()
    def __init__(self, parent=None):
        super(moveMus, self).__init__(parent)
        self.processing = True

        self.key = GetKeyboard()
        self.key.Get_Key.connect(self.Getkey)
        self.Delay = 0.01
        self.Delay_time = time.time() - self.Delay

        self.ScreenSaveTime = 60
        self.ScreenSaveTime_time = time.time()
        self.ScreenShield = False

        self.KeyTrigger: bool = False

        self.key.start()
        x, y = GetCursorPos()
        self.x_old = x
        self.y_old = y
        self.x_offset = 8
        self.y_offset = 8
        self.d = 0.0
    def run(self):
        while True:
            try:
                x,y = GetCursorPos()
            except:
                x = self.x_old
                y = self.y_old
            temp_time = time.time()
            if temp_time - self.Delay_time > self.Delay:
                if x != self.x_old or y != self.y_old:
                    self.WinMove(x, y)

                    self.ScreenSaveRelease()
                    self.ScreenSaveTime_time = temp_time

                if self.ScreenShield:
                    self.Set_WinShield.emit()
                    print("Win show")

                print(F"Screen {int(temp_time - self.ScreenSaveTime_time)}")
                self.Delay_time = temp_time

            if time.time() - self.ScreenSaveTime_time > self.ScreenSaveTime:
                self.ScreenShield = True
                self.PressKey()
                self.ScreenSaveTime_time = temp_time

            time.sleep(0.009)

    def ScreenSaveTime_Trigger(self):
        return time.time() - self.ScreenSaveTime_time > self.ScreenSaveTime

    def ScreenSaveRelease(self):
        if self.ScreenShield:
            self.Set_WinShield_Close.emit()
            self.ScreenShield = False
            print("Win close")

    def WinMove(self, x, y):
        r = np.arctan2(x, y)
        self.d = round((self.d + (r * 180 / np.pi)) / 2, 2)
        self.Set_MovePoint.emit(x + self.x_offset, y + self.y_offset, int(self.d))
        self.x_old = x
        self.y_old = y

    @pyqtSlot(str)
    def Getkey(self, name):
        if 'f19' != name:
            self.ScreenSaveRelease()
            print(name)
            self.ScreenSaveTime_time = time.time()
    def PressKey(self):
        self.KeyTrigger = True
        keybd_event(130, 0, 0, 0)
        keybd_event(130, 0, win32con.KEYEVENTF_KEYUP, 0)
        print("버튼 눌림")
        self.KeyTrigger = False

class GetKeyboard(QThread):
    Get_Key = pyqtSignal(str)
    def __init__(self):
        super(GetKeyboard, self).__init__()

    def run(self):
        while True:
            self.Get_Key.emit(keyboard.read_key())
            time.sleep(0.0001)

def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)

    sys._excepthook(exctype, value, traceback)

if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)

    MainWindow = mainWindow()
    MainWindow.show()

    app.exec()