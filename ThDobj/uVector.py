import numpy as np

class uVector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        ret = uVector()
        ret.x = self.x + other.x
        ret.y = self.y + other.y
        ret.z = self.z + other.z
        return ret

    def __sub__(self, other):
        ret = uVector()
        u = other

        ret.x = self.x - u.x
        ret.y = self.y - u.y
        ret.z = self.z - u.z
        return ret

    def __mul__(self, other):
        ret = uVector()
        u = other
        if type(u).__name__ == 'uVector':
            ret.x = self.y*u.z - self.z*u.y
            ret.y = self.z * u.x - self.x * u.z
            ret.z = self.x * u.y - self.y * u.x
        else:
            ret.x = self.x * u
            ret.y = self.y * u
            ret.z = self.z * u
        return ret

    def __truediv__(self, other):
        ret = uVector()
        ret.x = self.x/other
        ret.y = self.y/other
        ret.z = self.z/other

    def Rot(self, q):
        ret = uVector()
        r = np.radians(q)
        s = np.sin(r)
        c = np.cos(r)

        ret.x = c * self.x - s * self.y
        ret.y = s * self.x + c * self.y
        ret.z = self.z
        return ret

    def Norm(self):
        return np.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)