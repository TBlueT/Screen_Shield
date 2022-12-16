import ctypes

class vArray:
    m_pData = type
    m_nSize = 0
    stErr = ['' for i in range(100)]
    m_nPage = 0
    m_nMaxPage = 0
    bError = False
    def __init__(self, poly):
        self.CLICKPOLY = poly
        self.TYPE = self.CLICKPOLY
        self.ARG_TYPE = self.CLICKPOLY
        self.m_pData = None
        self.m_nSize = 0
        self.m_nMaxPage = 1024
        self.m_nPage = 0

        self.bError = False

    def __del__(self):
        self.RemoveAll()
    def GetSize(self):
        return self.m_nSize

    def add(self, arg, bOverwrite = False):
        nCurrent = self.m_nSize
        if self.m_pData == None:
            self.m_pData = [0 for i in range(ctypes.sizeof(self.TYPE))]


    def clear(self):
        self.m_pData = None
        self.m_nSize = 0


    def RemoveAll(self):
        self.m_pData = None
        self.m_nSize = 0
        self.m_nPage = 0
