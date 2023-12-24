#import time
#time.sleep(45)

import Network
import Instructions
import pickle
import traceback
import PygameTerminal as pt
import zlib

attemptIpList = [
    ["192.168.1.63", Network.PORT],#Main Pc
    [Network.SelfIp(), Network.PORT]#Self
]
def ConnectToServer():
    global soc
    soc = None
    for i in attemptIpList:
        pt.Print("Testing IP/PORT ("+i[0]+","+str(i[1])+")")
        try:
            soc = Network.Client(i[0], i[1])
            pt.Print("Success")
            break
        except Exception:
            pt.Print("Failed")
    if soc == None:
        raise Exception("Could not find a server")

ConnectToServer()

func = None
dataBuffer = None
compressReturn = False
compressArgs = False

def Start():
    global dataBuffer
    pt.Print("Starting")
    argBytes = soc.recive()
    if compressArgs:
        argBytes = zlib.decompress(argBytes)
    argList = pickle.loads(argBytes)
    try:
        result = func(argList)
    except Exception as e:
        result = Instructions.ERROR + "| "  + traceback.format_exc()
        print("Error -> " + result)
    pt.Print("Sending results")
    soc.send(Instructions.GOT_DATA)
    dataBuffer = result
def SetFunction():
    global func
    functionName = soc.recive(str)
    functionSourceCode = soc.recive(str)
    pt.Print(functionSourceCode)
    namespace = {}
    exec(functionSourceCode, namespace)
    func = namespace[functionName]
def GetData():
    byteList = pickle.dumps(dataBuffer)
    if compress:
        byteList = zlib.compress(byteList)
    soc.send(byteList)
def SetCompressionReturn():
    global compressReturn
    v = soc.recive(str)
    compressReturn = True if v == Instructions.TRUE else False
def SetCompressionArgs():
    global compressArgs
    v = soc.recive(str)
    compressArgs = True if v == Instructions.TRUE else False
def ExecInstruction():
    global compress
    soc.SetTimeOut(None)
    instruction = soc.recive(str)
    soc.SetTimeOut()
    if instruction == Instructions.SEND_FUNCTION:
        SetFunction()
    elif instruction == Instructions.START:
        Start()
    elif instruction == Instructions.GET_DATA:
        GetData()
    elif instruction == Instructions.SET_COMPRESSION_RETURN:
        SetCompressionReturn()
    elif instruction == Instructions.SET_COMPRESSION_ARGS:
        SetCompressionArgs()
    else:
        raise Exception("Failed invlaid insturciton -> " + instruction)

while 1:
    ExecInstruction()

