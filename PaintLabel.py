import time

from PyQt6.QtWidgets import QLabel, QGraphicsScene
from PyQt6.QtGui import QPainter

from ThDobj.uObj import *
from UiUpdateprocess import *

import random

class PaintLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.MainW = parent
        self.uiUpdate = UiUpdate(self)

        self.box = Obj(self)
        self.box.MakeBox(20,20,20)
        h = hMat()

        self.offset = 10
        self.box.H = h.Trans(uVector(-self.offset, -self.offset, -self.offset))*h.Trans(uVector(-20, -20, -20))# * h.RotZ(-45) * h.RotX(-125)

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
        self.a = 1 * (self.ran * 0.1)
        self.b = 1 * (self.ran2 * 0.1)
        self.c = 1 * (self.ran3 * 0.1)
        self.box.H = self.box.H * h.Trans(uVector(self.offset, self.offset, self.offset))
        self.box.H = self.box.H * h.RotX(self.a) * h.RotY(self.b) * h.RotZ(self.c)
        self.box.H = self.box.H * h.Trans(uVector(-self.offset, -self.offset, -self.offset))

        self.box.Update()
        self.box.Draw(qp)

        qp.end()
