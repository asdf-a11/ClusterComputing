import Server
import Function4 as Function

import pygame
import time

sx,sy = 600,600
dist = sx // 25
gasList = []
def InitGasList():
    x = 0
    while x <= sx:
        y = 0
        while y <= sy:
            gasList.append([x,y,0,0])
            y += dist
        x += dist
    
InitGasList()
inp = [
    sx,
    sy,
    3,
    [[200,200, 30, 0, 10]],
    20,
    10,
    1,
    gasList,
    0,
    len(gasList)
]

clientList = []

import pygame
import math
pygame.init()

window = pygame.display.set_mode((sx,sy))



def Draw(frameCounter):
    pygame.event.pump()
    pygame.draw.rect(window,(0,0,0),(0,0,sx,sy))
    out = gasList
    inp[7] = out
    for g in out:
        r = min(255, math.sqrt(g[2] ** 2 + g[3] ** 2) * 255)
        h = 0
        b = 255
        pygame.draw.circle(window,(r,h,b),(g[0], g[1]), 3)
    pygame.display.flip()
    pygame.image.save(window , str(frameCounter)+".png")

for frameCounter in range(200):    
    while 1:
        Server.UpdateClientList()
        for i in Server.clientList:
            if i.new:
                i.SetFunction(Function.func)
                i.SetCompression(False)
                i.new = False
        if len(Server.clientList) > 0:
            break
    start = time.time()
    inp[-2] = 0    
    size = len(gasList) // len(Server.clientList)
    print("size, ", size)
    for idx,i in enumerate(Server.clientList):        
        inp[-1] = inp[-2] + size
        print("start ", inp[-2], " end ", inp[-1])
        i.Start(inp)
        inp[-2] += size
    newGasList = []
    for idx,i in enumerate(Server.clientList):
        d = i.GetData()
        if type(d) == str:
            raise Exception(d)
        newGasList += d
    gasList = newGasList
    print("Time taken -> ", time.time() - start)
    Draw(frameCounter)









'''
import random
inp = [[],100]
for i in range(200):
    c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    inp[0].append([random.randint(0,200),random.randint(0,200), random.randint(5,10), c])

ex = False
while not ex:
    Server.UpdateClientList()
    for i in Server.clientList:
        if i.new:
            i.SetFunction(Function.func)
            i.SetCompression(True)
            i.new = False
            ex = True
Server.clientList[0].Start(inp)
imgList = Server.clientList[0].GetData()

import pygame, time
pygame.init()   
sx,sy = 200,200
window = pygame.display.set_mode((sx,sy))
while 1:
    for i in imgList:
        print(i.shape)
        pygame.event.pump()
        #pygame.surfarray.blit_array(window,i)
        #window.blit(,(0,0))
        for x in range(sx):
            for y in range(sy):
                pygame.draw.rect(window,(i[x][y][0],i[x][y][1],i[x][y][2]),(x,y,1,1))
        pygame.display.flip()
        #time.sleep(0.1)

'''
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


