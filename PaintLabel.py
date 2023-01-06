import time

from PyQt6.QtWidgets import QLabel, QGraphicsScene
from PyQt6.QtGui import QPainter

from ThDobj.uObj import *
from UiUpdateprocess import *

import random

class PaintLabel(QLabel):
    def __init__(self, parent:object = None, box_size:int=20, x_offset:int=0, y_offset:int=0, color:bool=False):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.MainW = parent
        self.uiUpdate = UiUpdate(self)

        self.color: bool = color
        self.BoxSize = box_size
        self.offset = 20
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.box = Obj(self, color=self.color)
        self.box.MakeBox(self.BoxSize,self.BoxSize,self.BoxSize)
        h = hMat()


        self.box.H = h.Trans(uVector(-self.offset - self.x_offset, -self.offset - self.y_offset, -self.offset))*h.Trans(uVector(-self.BoxSize/2, -self.BoxSize/2, -self.BoxSize/2))# * h.RotZ(-45) * h.RotX(-125)

        self.ran = 0
        self.ran2 = 0
        self.ran3 = 0

        self.Delay = 5
        self.Delay_time = time.time() - self.Delay
        self.uiUpdate.start()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        h = hMat()

        if time.time() - self.Delay_time > self.Delay:
            random.seed()
            self.ran = random.randrange(-20, 20)
            random.seed()
            self.ran2 = random.randrange(-20, 20)
            random.seed()
            self.ran3 = random.randrange(-20, 20)
            self.Delay_time = time.time()
        a = 1 * (self.ran * 0.1)
        b = 1 * (self.ran2 * 0.1)
        c = 1 * (self.ran3 * 0.1)
        self.box.H = self.box.H * h.Trans(uVector(self.BoxSize/2, self.BoxSize/2, self.BoxSize/2))
        self.box.H = self.box.H * h.RotX(a) * h.RotY(b) * h.RotZ(c)
        self.box.H = self.box.H * h.Trans(uVector(-self.BoxSize/2, -self.BoxSize/2, -self.BoxSize/2))

        self.box.Update()
        self.box.Draw(qp)

        qp.end()
