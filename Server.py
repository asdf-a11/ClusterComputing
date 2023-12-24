import Network
import pickle
import Instructions
#import platform
#import os
import inspect
import zlib
import time

soc = Network.Server()
soc.setListen(10000)

#PYTHON_NAME = "python"
#if platform.system() == "Linux":
#    PYTHON_NAME = "python3"

def TimeFunction(argList):
    import time
    start = time.time()
    counter = 1
    while time.time() - start < 0.25:
        num = counter
        while(num != 1):
            if((num%2)==0):
                num = num // 2 
            else:
                num = (num*3) + 1
        counter += 1
    return [counter]

class Client():
    def __init__(self):
        self.new = True
        self.func = None
        self.networkClient = None
        self.gotData = False
        self.data = None
        self.compressionReturn = False
        self.compressArgs = False
        self.taskStartTime = None
        self.taskEndTime = None
        self.taskDuration = None
        self.flops = None
    def MeasureProcSpeed(self):
        self.SetFunction(TimeFunction)
        self.Start([])
        self.flops = self.GetData()[0]
        print("Client flop count = ", self.flops)
    def SetFunction(self, func):
        functionName = func.__name__
        functionSourceCode = inspect.getsource(func)
        self.networkClient.send(Instructions.SEND_FUNCTION)
        self.networkClient.send(functionName)
        self.networkClient.send(functionSourceCode)
    def Start(self, argList):
        self.taskStartTime = time.time()
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
        if self.compressionReturn:
            recivedBytes = zlib.decompress(recivedBytes)
        data = pickle.loads(recivedBytes)
        self.taskEndTime = time.time()
        self.taskDuration = self.taskEndTime - self.taskStartTime
        return data     


clientList = []

def UpdateClientList():
    for i in soc.clientList:
        if i.new == True:
            i.new = False
            c = Client()
            c.networkClient = i
            c.MeasureProcSpeed()
            clientList.append(c)









