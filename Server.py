import Network
import pickle
import Instructions
#import platform
#import os
import inspect
import zlib

soc = Network.Server()
soc.setListen(10000)

#PYTHON_NAME = "python"
#if platform.system() == "Linux":
#    PYTHON_NAME = "python3"

class Client():
    def __init__(self):
        self.new = True
        self.func = None
        self.networkClient = None
        self.gotData = False
        self.data = None
        self.compression = False
    def SetFunction(self, func):
        functionName = func.__name__
        functionSourceCode = inspect.getsource(func)
        self.networkClient.send(Instructions.SEND_FUNCTION)
        self.networkClient.send(functionName)
        self.networkClient.send(functionSourceCode)
    def Start(self, argList):
        self.networkClient.send(Instructions.START)
        self.networkClient.send(len(argList))
        for i in argList:
            self.networkClient.send(pickle.dumps(i))
    def SetCompression(self, TorF):
        self.networkClient.send(Instructions.SET_COMPRESSION)
        self.networkClient.send(Instructions.TRUE if TorF else Instructions.FALSE)
        self.compression = TorF
    def GetData(self):
        while 1:
            gotDataMsg = self.networkClient.recive(str)
            if gotDataMsg == Instructions.GOT_DATA:
                break
        self.networkClient.send(Instructions.GET_DATA)
        recivedBytes = self.networkClient.recive()
        if self.compression:
            recivedBytes = zlib.decompress(recivedBytes)
        data = pickle.loads(recivedBytes)
        return data     


clientList = []

def UpdateClientList():
    for i in soc.clientList:
        if i.new == True:
            i.new = False
            c = Client()
            c.networkClient = i
            clientList.append(c)









