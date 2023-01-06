from PyQt6.QtGui import QPainterPath, QPen, QBrush, QColor
from PyQt6.QtCore import Qt

from ThDobj.uVector import *
import random

class uPolygon:
    def __init__(self, f=-1, s=-1, t=-1, color:bool=False):
        self.f = f
        self.s = s
        self.t = t
        #self.color = '#00aa00'
        self.color:bool = color
        self.c = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        self.bDraw = False

    def SetColor(self, color=None):
        if color != None:
            self.color = color

    def inpu(self, f, s, t):
        self.f = f
        self.s = s
        self.t = t
        print(self.f, self.s, self.t)

    def Draw(self, qp, pVer, x=0,y=0):
        path = QPainterPath()

        path.moveTo(x - pVer[self.f].x, y - pVer[self.f].y)
        path.lineTo(x - pVer[self.s].x, y - pVer[self.s].y)
        path.lineTo(x - pVer[self.t].x, y - pVer[self.t].y)
        path.lineTo(x - pVer[self.f].x, y - pVer[self.f].y)
        qp.setPen(QPen(Qt.GlobalColor.blue, 3.5))
        if self.color:
            qp.setBrush(QBrush(QColor(self.c)))
        qp.drawPath(path)

    def Click(self, pTemp, pt):
        o  = uVector(pt.x, pt.y, 0)

        vf = uVector()
        vs = uVector()
        vt = uVector()
        n  = uVector()

        vf = pTemp[self.f] - o
        vs = pTemp[self.s] - o
        vt = pTemp[self.t] - o
        vf.z = 0
        vs.z = 0
        vt.z = 0


        n = vf*vs
        sgn = 1 if n.z > 0 else -1
        if sgn < 0:
            return False

        n = vs * vt
        sgn2 = 1 if n.z > 0 else -1
        if sgn * sgn2 < 0:
            return False

        n = vt * vf
        sgn3 = 1 if n.z > 0 else -1
        if sgn * sgn3 < 0:
            return False

        return True