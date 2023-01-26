#-*- coding: utf-8 -*-

from PyQt6 import QtCore, QtGui, QtTest

import socket, time, datetime
#from Packets import *

class UDPPro(QtCore.QThread):
    def __init__(self, parent=None):
        super(UDPPro, self).__init__(parent)
        self.Working = True
        self.mainWindow = parent

        self.Rssi:int = 0

        self.rssi_L:int = 11
        self.rssi_list: list = [0 for _ in range(self.rssi_L)]


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 7720))

    def run(self):
        while self.Working:
            data, addr = self.sock.recvfrom(1500)
            temp_data = data.decode().split(',')
            temp_addr = temp_data[1]
            temp_rssi = int(temp_data[len(temp_data)-1])

            if temp_addr.find('020a180a') > 0:
                self.rssi_list[self.rssi_L-1] = temp_rssi
                for i in range(self.rssi_L-1):
                    self.rssi_list[i] = self.rssi_list[i+1]
                    self.Rssi += self.rssi_list[i]
                temp = self.Rssi/(self.rssi_L-1)
                self.Rssi = temp

                #print(temp_rssi)
                #self.Rssi = temp_rssi
            #print(temp_addr, temp_rssi)