from ThDobj.uPolygon import *
from ThDobj.uCam import *

import ctypes

class Obj:
    def __init__(self, parent=None):
        self.daemon = True
        self.run_stop = True
        self.main = parent

        self.Hg = hMat()
        self.H = hMat()
        self.q = uVector()

        #self.pCam = self.main.ucam
        self.pVer = None
        self.pTemp = None
        self.pPoly = None

        self.nVer = 0
        self.nPoly = 0

        self.nSelected = 0



    def Alloc(self, nv, np):
        self.Close()

        self.nVer = nv
        self.nPoly = np

        self.pVer = [uVector()]*nv
        self.pTemp = [uVector()]*nv
        self.pPoly = [uPolygon()]*np

    def Close(self):
        if self.pVer:
            self.pVer = None
        if self.pPoly:
            self.pPoly = None
        if self.pTemp:
            self.pTemp = None

    def Update(self, ):
        for i in range(0,self.nVer):
            self.pTemp[i] = self.Hg*self.H*self.pVer[i]
            #self.pTemp[i] = pCam.Projection(self.pTemp[i])

        for i in range(0,self.nPoly):
            f = self.pPoly[i].f
            s = self.pPoly[i].s
            t = self.pPoly[i].t

            A = self.pTemp[t]-self.pTemp[s]
            B = self.pTemp[f]-self.pTemp[s]
            if (A*B).z>0:
                self.pPoly[i].bDraw = True
            else:
                self.pPoly[i].bDraw = False


    def Draw(self, qp, x=0, y=0):

        for i in range(self.nPoly):
            if self.pPoly[i].bDraw:
                self.pPoly[i].Draw(qp, self.pTemp, x, y)

    def MakeBox(self, a, b, c):
        self.Alloc(8, 12)

        self.pVer[0] = uVector(0, 0, 0)
        self.pVer[1] = uVector(a, 0, 0)
        self.pVer[2] = uVector(a, 0, b)
        self.pVer[3] = uVector(0, 0, b)
        self.pVer[4] = uVector(0, c, 0)
        self.pVer[5] = uVector(a, c, 0)
        self.pVer[6] = uVector(a, c, b)
        self.pVer[7] = uVector(0, c, b)

        self.pPoly[0] = uPolygon(0, 1, 2)
        self.pPoly[1] = uPolygon(0, 2, 3)
        self.pPoly[2] = uPolygon(6, 2, 1)
        self.pPoly[3] = uPolygon(6, 1, 5)
        self.pPoly[4] = uPolygon(4, 0, 3)
        self.pPoly[5] = uPolygon(4, 3, 7)
        self.pPoly[6] = uPolygon(7, 3, 2)
        self.pPoly[7] = uPolygon(7, 2, 6)
        self.pPoly[8] = uPolygon(5, 1, 0)
        self.pPoly[9] = uPolygon(5, 0, 4)
        self.pPoly[10] = uPolygon(4, 7, 6)
        self.pPoly[11] = uPolygon(4, 6, 5)

    def MakeCyl(self, r, h ,n):
        self.Alloc(2*n+2, 2*n*2)

        x = 0.0
        y = 0.0
        dq = 360 / n

        for i in range(n):
            x = r * np.cos(np.radians(i*dq))
            y = r * np.sin(np.radians(i*dq))

            self.pVer[i] = uVector(x,y,0)
            self.pVer[i + n] = uVector(x,y,h)

        self.pVer[n*2+1] = uVector(0,0,h)

        j = 0
        for i in range(n):

            next = i+1
            if next >= n:
                next = 0

            self.pPoly[j] = uPolygon(i, next, next+n)
            j += 1
            self.pPoly[j] = uPolygon(i, next+n, i + n)
            j += 1
            self.pPoly[j] = uPolygon(n*2, next, i)
            j += 1
            self.pPoly[j] = uPolygon((n*2)+1, i+n, next+n)
            j += 1

    def MakeBlock(self, color=None):
        V = self.main.V
        P = self.main.P

        np = len(P)
        nv = len(V)
        self.Alloc(int(nv / 3), int(np / 3))

        n = 0
        for i in range(0, nv, 3):
            self.pVer[n] = uVector(V[i], V[i + 1], V[i + 2])
            n += 1

        n = 0
        for i in range(0, np, 3):
            f = P[i] - 1
            s = P[i + 1] - 1
            t = P[i + 2] - 1
            self.pPoly[n] = uPolygon(f, s, t)
            self.pPoly[n].SetColor(color)
            n += 1


    def Click(self, pt):
        buf = [[0,0] for i in range(self.nPoly)]
        for i in range(self.nPoly):
            if self.pPoly[i].Click(self.pTemp, pt) == True:

                nf = self.pPoly[i].f
                ns = self.pPoly[i].s
                nt = self.pPoly[i].t

                f = uVector(self.pTemp[nf].x, self.pTemp[nf].y, 0)
                s = uVector(self.pTemp[ns].x, self.pTemp[ns].y, 0)
                t = uVector(self.pTemp[nt].x, self.pTemp[nt].y, 0)
                p = uVector(pt.x, pt.y, 0)

                a = (f - s).Norm()
                b = (f - p).Norm()
                c = (s - p).Norm()
                m = (a + b + c) / 2
                s1 = np.sqrt(m * (m - a) * (m - b) * (m - c))

                a = (s - t).Norm()
                b = (s - p).Norm()
                c = (t - p).Norm()
                m = (a + b + c) / 2
                s2 = np.sqrt(m * (m - a) * (m - b) * (m - c))

                a = (t - f).Norm()
                b = (t - p).Norm()
                c = (f - p).Norm()
                m = (a + b + c) / 2
                s3 = np.sqrt(m * (m - a) * (m - b) * (m - c))

                S = s1 + s2 + s3
                w1 = s1 / S
                w2 = s2 / S
                w3 = s3 / S

                z = w1 * self.pTemp[nf].z + w2 * self.pTemp[ns].z + w3 * self.pTemp[nt].z

                buf[i][0] = i
                buf[i][1] = z

        minn = 0
        mindata = 0
        for i in range(self.nPoly):
            if buf[i][1] > mindata:
                mindata = buf[i][1]
                minn = i

        print(minn, mindata)

        print(self.pTemp[minn].x, self.pTemp[minn].y, self.pTemp[minn].z)



class CLICKPOLY:
    _fields_ = [
        ("nPolygon", ctypes.c_int),
        ("z", ctypes.c_float)
    ]