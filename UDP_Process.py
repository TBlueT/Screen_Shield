#-*- coding: utf-8 -*-

from PyQt6 import QtCore, QtGui, QtTest

import socket, time, datetime, math
#from Packets import *

class UDPPro(QtCore.QThread):
    def __init__(self, parent=None):
        super(UDPPro, self).__init__(parent)
        self.Working = True
        self.mainWindow = parent

        self.Rssi:int = 0

        self.fc: int = 20
        self.dt: float = 1/1000.0
        self.lambde: float = 2*math.pi*self.fc*self.dt
        self.x: float = 0.0
        self.x_f: float = 0.0
        self.x_fold: float = 0.0


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 7720))

    def run(self):
        while self.Working:
            data, addr = self.sock.recvfrom(1500)
            temp_data = data.decode().split(',')
            temp_addr = temp_data[1]
            temp_rssi = int(temp_data[len(temp_data)-1])

            if temp_addr.find('020a180a') > 0:
                temp = self.lambde/(1+self.lambde)*temp_rssi+1/(1+self.lambde)*self.x_fold
                self.x_fold = temp
                self.Rssi = temp
            time.sleep(0.1)
                #print(temp_rssi)
                #self.Rssi = temp_rssi
            #print(temp_addr, temp_rssi)