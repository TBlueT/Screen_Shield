from ThDobj.hVector import *

class hMat:
	def __init__(self):
		self.v = [0.0]*16
		self.v[0] = 1
		self.v[5] = 1
		self.v[10] = 1
		self.v[15] = 1

	def Trans(self, u):
		if type(u).__name__ == 'uVector':
			ret = hMat()
			ret.v[12] = u.x
			ret.v[13] = u.y
			ret.v[14] = u.z
		else:
			ret = hMat()
			ret.v[12] = u[0]
			ret.v[13] = u[1]
			ret.v[14] = u[2]
		return ret

	def RotX(self, q):
		ret = hMat()
		r = np.radians(q)
		c = np.cos(r)
		s = np.sin(r)

		ret.v[5] = c
		ret.v[6] = s
		ret.v[9] = -s
		ret.v[10] = c
		return ret


	def RotY(self, q):

		ret = hMat()
		r = np.radians(q)
		c = np.cos(r)
		s = np.sin(r)

		ret.v[0] = c
		ret.v[2] = -s
		ret.v[8] = s
		ret.v[10] = c
		return ret


	def RotZ(sefl, q):
		ret = hMat()
		r = np.radians(q)
		c = np.cos(r)
		s = np.sin(r)

		ret.v[0] = c
		ret.v[1] = s
		ret.v[4] = -s
		ret.v[5] = c
		return ret

	def __mul__(self, other):
		if type(other).__name__ == 'hMat':
			v = self.v
			m = other
			ret = hMat()
			ret.v[0] = v[0] * m.v[0] + v[4] * m.v[1] + v[8] * m.v[2] + v[12] * m.v[3]
			ret.v[1] = v[1] * m.v[0] + v[5] * m.v[1] + v[9] * m.v[2] + v[13] * m.v[3]
			ret.v[2] = v[2] * m.v[0] + v[6] * m.v[1] + v[10] * m.v[2] + v[14] * m.v[3]
			ret.v[3] = v[3] * m.v[0] + v[7] * m.v[1] + v[11] * m.v[2] + v[15] * m.v[3]

			ret.v[4] = v[0] * m.v[4] + v[4] * m.v[5] + v[8] * m.v[6] + v[12] * m.v[7]
			ret.v[5] = v[1] * m.v[4] + v[5] * m.v[5] + v[9] * m.v[6] + v[13] * m.v[7]
			ret.v[6] = v[2] * m.v[4] + v[6] * m.v[5] + v[10] * m.v[6] + v[14] * m.v[7]
			ret.v[7] = v[3] * m.v[4] + v[7] * m.v[5] + v[11] * m.v[6] + v[15] * m.v[7]

			ret.v[8] = v[0] * m.v[8] + v[4] * m.v[9] + v[8] * m.v[10] + v[12] * m.v[11]
			ret.v[9] = v[1] * m.v[8] + v[5] * m.v[9] + v[9] * m.v[10] + v[13] * m.v[11]
			ret.v[10] = v[2] * m.v[8] + v[6] * m.v[9] + v[10] * m.v[10] + v[14] * m.v[11]
			ret.v[11] = v[3] * m.v[8] + v[7] * m.v[9] + v[11] * m.v[10] + v[15] * m.v[11]

			ret.v[12] = v[0] * m.v[12] + v[4] * m.v[13] + v[8] * m.v[14] + v[12] * m.v[15]
			ret.v[13] = v[1] * m.v[12] + v[5] * m.v[13] + v[9] * m.v[14] + v[13] * m.v[15]
			ret.v[14] = v[2] * m.v[12] + v[6] * m.v[13] + v[10] * m.v[14] + v[14] * m.v[15]
			ret.v[15] = v[3] * m.v[12] + v[7] * m.v[13] + v[11] * m.v[14] + v[15] * m.v[15]
			return ret

		elif type(other).__name__ == 'hVector':
			u = other
			v = self.v
			ret = hVector()
			ret.x = v[0] * u.x + v[4] * u.y + v[8] * u.z + v[12] * u.h
			ret.y = v[1] * u.x + v[5] * u.y + v[9] * u.z + v[13] * u.h
			ret.z = v[2] * u.x + v[6] * u.y + v[10] * u.z + v[14] * u.h
			ret.h = v[3] * u.x + v[7] * u.y + v[11] * u.z + v[15] * u.h
			return ret

		elif type(other).__name__ == 'uVector':
			v = self.v
			u = other
			ret = uVector()
			ret.x = v[0] * u.x + v[4] * u.y + v[8] * u.z + v[12]
			ret.y = v[1] * u.x + v[5] * u.y + v[9] * u.z + v[13]
			ret.z = v[2] * u.x + v[6] * u.y + v[10] * u.z + v[14]
			return ret

	def O(self):
		return uVector(self.v[12], self.v[13], self.v[14])


	def Scale(self, f):
		ret = hMat()
		ret.v[0] = f
		ret.v[5] = f
		ret.v[10] = f
		return ret

	def set(self, other):
		self.v = [0.0] * 16
		self.v[0] = 1
		self.v[5] = 1
		self.v[10] = 1
		self.v[15] = 1
		self.v[12] = other.x
		self.v[13] = other.y
		self.v[14] = other.z
