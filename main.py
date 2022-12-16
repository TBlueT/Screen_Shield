# -*- coding: utf-8 -*-
import sys
import os, time
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6 import uic

from win32api import GetCursorPos, keybd_event, GetKeyState
import win32con
from PaintLabel import *

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.view = PaintLabel(self)
        self.view.resize(40,40)
        layout.addWidget(self.view)

        self.setLayout(layout)

        self.mouseMove = moveMus()
        self.mouseMove.Set_MovePoint.connect(self.Set_MovePoint)

        self.mouseMove.start()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_Disabled, True)
        self.resize(40, 40)

    @pyqtSlot(int, int, int)
    def Set_MovePoint(self, x, y, d):
        self.move(x, y)

    @pyqtSlot(int, int)
    def Set_reSize(self, x, y):
        self.resize(x,y)

class Shield(QDialog):
    def __init__(self, x, y):
        super(Shield, self).__init__()
        self.Win_x = x
        self.Win_y = y
        self.resize(self.Win_x, self.Win_y)

        layout = QVBoxLayout()

        self.view = PaintLabel(self)
        self.view.resize(self.Win_x, self.Win_y)
        layout.addWidget(self.view)

        self.setLayout(layout)



class moveMus(QThread):
    Set_MovePoint = pyqtSignal(int, int, int)
    Set_reSize = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(moveMus, self).__init__(parent)
        self.processing = True

        self.Delay = 0.01
        self.Delay_time = time.time() - self.Delay

        self.ScreenSaveTime = 240
        self.ScreenSaveTime_time = time.time()
        self.ScreenShield = False

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
                    self.ScreenShield = False
                    self.ScreenSaveTime_time = temp_time

                if self.ScreenShield:
                    pass#self.WinReSize()
                else:
                    self.WinMove(x, y)
                print(F"Screen {int(temp_time - self.ScreenSaveTime_time)}")
                self.Delay_time = temp_time

            if temp_time - self.ScreenSaveTime_time > self.ScreenSaveTime:
                self.ScreenShield = True
                self.PressKey()
                self.ScreenSaveTime_time = temp_time

            time.sleep(0.005)

    def WinMove(self, x, y):
        r = np.arctan2(x, y)
        self.d = round((self.d + (r * 180 / np.pi)) / 2, 2)
        self.Set_MovePoint.emit(x + self.x_offset, y + self.y_offset, int(self.d))
        self.x_old = x
        self.y_old = y

    def WinReSize(self, x, y):
        self.Set_reSize(x, y)

    def PressKey(self):
        keybd_event(17, 0, 0, 0)
        keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        print("버튼 눌림")


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