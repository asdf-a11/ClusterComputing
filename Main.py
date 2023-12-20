import Server
import Function



import random
inp = [[],1]
for i in range(3):
    c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    inp[0].append([random.randint(0,400),random.randint(0,400), random.randint(5,400), c])

ex = False
while not ex:
    Server.UpdateClientList()
    for i in Server.clientList:
        if i.new:
            i.SetFunction(Function.func)
            i.new = False
            ex = True
Server.clientList[0].Start(inp)
imgList = Server.clientList[0].GetData()

import pygame, time
pygame.init()   
sx,sy = 400,400
window = pygame.display.set_mode((sx,sy))
while 1:
    for i in imgList:
        pygame.event.pump()
        window.blit(pygame.surfarray.blit_array(i),(0,0))
        pygame.display.flip()
        time.sleep(0.1)


'''
run = True
DATA_SIZE = 5
number = 1
num = 0
while run:
    Server.UpdateClientList()
    for i in Server.clientList:
        if i.new:
            i.SetFunction(Function.func)
            i.new = False
    for i in Server.clientList:
        i.Start([number])
        number += DATA_SIZE
    for i in Server.clientList:
        recivedData = i.GetData()
        print(recivedData)
        num += recivedData    
    print(num)
'''


