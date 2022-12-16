from ThDobj.hMat import *

import numpy as np

class uCam:
    def __init__(self):
        self.P = hMat()
        self.S = hMat()
        self.R = hMat()
        self.T = hMat()
        self.q = uVector()

        self.n = 1
        self.f = 65535
        self.angle = 90
        self.aspect = 1

        self.z1 = (self.n+self.f)/(self.f-self.n)
        self.z2 = (self.n*self.f)/(self.f-self.n)
        self.ct = 1./np.tan(np.radians(self.angle)/2)

        self.P.v[0] = self.ct/self.aspect
        self.P.v[5] = self.ct
        self.P.v[10] = -self.z1
        self.P.v[11] = -1
        self.P.v[14] = -2*self.z2
        self.P.v[15] = 1

        self.S = self.S.Scale(320)

        self.T.set(uVector(0,0,-300))
        self.q = uVector()

    def Projection(self, t):

        t = self.R*t

        t = self.T*t

        z = t.z
        t = self.P*t

        t = t*(-1./z)

        t = self.S*t

        return t

pCam = uCam()