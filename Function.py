import Network


def func(argList):
    print(argList)
    import math
    import pygame
    import copy
    import time
    import numpy as np
    pygame.init()
    STEP = 10
    sx,sy = 100,100
    window = pygame.display.set_mode((sx,sy))
    it = argList[1]
    GRAV = 9.81
    G = 6.67# * 10 ** -11 
    class Planet():
        def __init__(self, x, y, mass, colour):
            self.x = x; self.y = y
            self.ax,self.ay = 0,0
            self.vx,self.vy = 0,0
            self.mass = mass
            self.colour = colour
        def GetDist_nonSqrt(self, toX, toY):
            return (toX - self.x) ** 2 + (toY - self.y) ** 2
        def SetAccZero(self):
            self.ax = 0
            self.ay = 0
        def UpdateAcc(self):            
            for p in planetList:
                diffX, diffY = (p.x - self.x), (p.y - self.y)
                r2 = max(diffX ** 2 + diffY ** 2, 10**2)
                if r2 == 0: continue
                r = math.sqrt(r2)
                accMag = G * self.mass / r
                
                unitX = diffX / r
                unitY = diffY / r
                p.ax -= unitX * accMag
                p.ay -= unitY * accMag
        def UpdatePos(self):
            self.vx += self.ax / STEP ** 2
            self.vy += self.ay / STEP ** 2
            self.x += self.vx / STEP
            self.y += self.vy / STEP
        def Draw(self):
            r,g,b = self.colour
            g = 0
            b = min(255, self.mass ** 4)
            r = min(255,math.log2(math.sqrt(max(self.vx **2 + self.vy ** 2,1))) * 50)
            pygame.draw.circle(window,(int(r),int(g),int(b)),(int(self.x), int(self.y)), int(max(2, math.log2(self.mass))))

    planetList = []
    for i in argList[0]:
        planetList.append(Planet(i[0], i[1], i[2], i[3]))    
    out = []
    for i in range(it):
        print("Frame ", i)
        pygame.event.pump()
        pygame.draw.rect(window,(0,0,0),(0,0,sx,sy))
        for p in planetList:
            p.SetAccZero()
        for p in planetList:
            p.UpdateAcc()
        for p in planetList:
            p.UpdatePos()
        for p in planetList:
            p.Draw()
        pygame.display.update()
        memory_surface = pygame.Surface((sx,sy))
        memory_surface.blit(window, (0, 0))
        out.append(pygame.surfarray.array3d(memory_surface))
        time.sleep(0.2)
    pygame.quit()
    return out

if __name__ == "__main__":
    #x, y, mass, colour
    import random
    inp = [[],10]
    for i in range(200):
        c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        inp[0].append([random.randint(0,100),random.randint(0,100), random.randint(5,400), c])
    imgList = func(inp)
    import pygame, time
    pygame.init()   
    sx,sy = 400,400
    window = pygame.display.set_mode((sx,sy))
    for i in imgList:
        pygame.event.pump()
        window.blit(pygame.surfarray.blit_array(i),(0,0))
        pygame.display.flip()
        time.sleep(0.1)