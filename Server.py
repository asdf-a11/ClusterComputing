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
        self.compressionReturn = False
        self.compressArgs = False
    def SetFunction(self, func):
        functionName = func.__name__
        functionSourceCode = inspect.getsource(func)
        self.networkClient.send(Instructions.SEND_FUNCTION)
        self.networkClient.send(functionName)
        self.networkClient.send(functionSourceCode)
    def Start(self, argList):
        self.networkClient.send(Instructions.START)
        assert type(argList) == list
        argListBytes = pickle.dumps(argList)
        if self.compressArgs:
            argListBytes = zlib.compress(argListBytes)
        self.networkClient.send(argListBytes)
    def SetCompressionArgs(self, TorF):
        self.networkClient.send(Instructions.SET_COMPRESSION_ARGS)
        self.networkClient.send(Instructions.TRUE if TorF else Instructions.FALSE)
        self.compressionArgs = TorF
    def SetCompressionReturn(self, TorF):
        self.networkClient.send(Instructions.SET_COMPRESSION_RETURN)
        self.networkClient.send(Instructions.TRUE if TorF else Instructions.FALSE)
        self.compressionReturn = TorF
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









