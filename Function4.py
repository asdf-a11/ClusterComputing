def func(argList):
    print("Starting")
    sx,sy = argList[0], argList[1]
    pSize = argList[2]
    forceData = argList[3]
    dist = argList[4]
    sep = argList[5]
    mass = argList[6]
    gasData = argList[7]
    startGasIdx = argList[8]
    endGasIdx = argList[9]


    import math



    renderPSize = max(1, pSize)
    forceList = []
    gasList = []

    class Force():
        def __init__(self, posx, posy, mag, start, end):
            self.posx = posx
            self.posy = posy
            self.mag = mag
            self.start = start
            self.end = end    
    class Gas():
        def __init__(self, posx, posy, vx, vy):
            self.posx = posx
            self.posy = posy
            self.ax, self.ay = 0,0
            self.vx, self.vy = vx,vy
            self.oldx, self.oldy = self.posx, self.posy
        def SetOldPos(self):
            self.oldx = self.posx
            self.oldy = self.posy
        def GetDistance_nonSqrt(self, gas):
            return (self.posx - gas.posx) ** 2 + (self.posy - gas.posy) ** 2
        def SetAccZero(self):
            self.ax, self.ay = 0,0
        def UpdateForce(self):
            for f in forceList:
                distx = (self.posx - f.posx)
                disty = (self.posy - f.posy)
                r2 = max(renderPSize,distx ** 2 + disty ** 2)
                r = math.sqrt(r2)
                #a = s/(r2*m)
                aMag = f.mag/(r2 * mass)
                self.ax += aMag / r * distx
                self.ay += aMag / r * disty
        def UpdateOtherGas(self):
            for og in gasList:
                distx = (self.posx - og.posx)
                disty = (self.posy - og.posy)
                r2 = max(0.5,distx ** 2 + disty ** 2)
                if r2 > 10000:
                    continue
                if og != self:                     
                    r = math.sqrt(r2)
                    #a = s/(r2*m)
                    aMag = sep/(r2 * mass)
                    self.ax += aMag / r * distx
                    self.ay += aMag / r * disty
        def Update(self):
            self.oldvx,self.oldvy = self.vx, self.vy
            to = max(1,int(math.sqrt(self.oldvx ** 2 + self.oldvy ** 2) / math.sqrt(2)))
            for i in range(0,to):
                self.SetAccZero()
                self.UpdateForce()
                self.UpdateOtherGas()
                self.UpdateVelocity(to)
        def UpdateVelocity(self, stepCounter = 1):
            self.vx += self.ax / stepCounter
            self.vy += self.ay / stepCounter
        def UpdatePos(self):
            self.posx += self.vx
            self.posy += self.vy

            if self.posx > sx:
                self.posx = sx
                self.vx *= -1
            if self.posx < 0:
                self.posx = 0
                self.vx *= -1
            if self.posy > sy:
                self.posy = sy
                self.vy *= -1
            if self.posy < 0:
                self.posy = 0
                self.vy *= -1

    def LoadForces():
        for d in forceData:
            f = Force(d[0],d[1],d[2],d[3],d[4])
            forceList.append(f)
    def LoadGasData():
        for d in gasData:
            g = Gas(d[0],d[1],d[2],d[3])
            gasList.append(g)
    def UpdateGas():
        for i in range(startGasIdx, endGasIdx):
            g = gasList[i]
            g.Update()
            if i % 100:
                print(int((i-startGasIdx)/endGasIdx * 100), "%")
        for i in range(startGasIdx, endGasIdx):
            gasList[i].UpdatePos()
    def PrintTotalVelocity():
        vx,vy = 0,0
        for g in gasList:
            vx += g.vx
            vy += g.vy
        print("vx,vy", vx,", ", vy)
    LoadForces()
    LoadGasData()

    UpdateGas()
    PrintTotalVelocity()

    out = []
    for i in range(startGasIdx, endGasIdx):
        g = gasList[i]
        out.append([g.posx,g.posy, g.vx,g.vy])
    return out



if __name__ == "__main__":
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
    # posx, posy, mag, start, end)
    '''
    sx = argList[0]
    sy = argList[1]
    pSize = argList[2]
    forceData = argList[3]
    dist = argList[4]
    sep = argList[4]
    mass = argList[5]
    gasData = argList[6]
    startGasIdx = argList[7]
    endGasIdx = argList[8]
    '''
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


    import pygame
    import math
    pygame.init()
    window = pygame.display.set_mode((sx,sy))
    while 1:
        pygame.event.pump()
        pygame.draw.rect(window,(0,0,0),(0,0,sx,sy))
        out = func(inp)
        inp[7] = out
        for g in out:
            r = min(255, math.sqrt(g[2] ** 2 + g[3] ** 2) * 255)
            h = 0
            b = 255
            pygame.draw.circle(window,(r,h,b),(g[0], g[1]), 3)
        pygame.display.flip()
        
