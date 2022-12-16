from ThDobj.uVector import *


class hVector(uVector):
	def __init__(self):
		super(hVector, self).__init__()
		self.h = 1

	def hVector(self, a):
		if type(a).__name__ == 'hVector':
			v = a
			ret = hVector()
			ret.x = self.x + v.x
			ret.y = self.y + v.y
			ret.z = self.z + v.z
			ret.h = self.h + v.h
			return ret
		else:
			if type(a[0]).__name__ == 'uVector':
				v = a[0]
				self.x = v.x
				self.y = v.y
				self.z = v.z
				self.h = a[1]
			else:
				x = a[0]
				y = a[1]
				z = a[2]
				h = a[3]
