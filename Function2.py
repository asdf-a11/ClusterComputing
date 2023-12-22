def func(argList):    
    pixelStartId = argList[0]
    pixelEndId = argList[1]
    sphereDataList = argList[2]
    camPos = argList[3]
    screenx = argList[4]
    screeny = argList[5]
    import numpy as np

    MAX_DIST = 10000.0
    BOUNCE_MAX = 3
    SAMPLE_COUNT = 1
    FOV = 90.0

    def normalize(x):
        x /= np.linalg.norm(x)
        return x
    def IntersectSphere(O, D, S, R):
        # Return the distance from O to the intersection of the ray (O, D) with the 
        # sphere (S, R), or +inf if there is no intersection.
        # O and S are 3D points, D (direction) is a normalized vector, R is a scalar.
        a = np.dot(D, D)
        OS = O - S
        b = 2 * np.dot(D, OS)
        c = np.dot(OS, OS) - R * R
        disc = b * b - 4 * a * c
        if disc > 0:
            distSqrt = np.sqrt(disc)
            q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
            t0 = q / a
            t1 = c / q
            t0, t1 = min(t0, t1), max(t0, t1)
            if t1 >= 0:
                return t1 if t0 < 0 else t0
        return np.inf
    class Sphere():
        def __init__(self, pos, size, colour):
            self.pos = pos
            self.size = size
            self.colour = colour
        def Intersect(self, rayOrg, rayDir):
            return IntersectSphere(rayOrg, rayDir, self.pos, self.size)
    def IntersectPlane(O, D, P, N):
        # Return the distance from O to the intersection of the ray (O, D) with the 
        # plane (P, N), or +inf if there is no intersection.
        # O and P are 3D points, D and N (normal) are normalized vectors.
        denom = np.dot(D, N)
        if np.abs(denom) < 1e-6:
            return np.inf
        d = np.dot(P - O, N) / denom
        if d < 0:
            return np.inf
        return d
    class Plane():
        def __init__(self, pos, size, colour, normal):
            self.pos = np.array(pos)
            self.size = size
            self.colour = np.array(colour,dtype=np.float32)
            self.normal = np.array(normal)
        def Intersect(self, rayOrg, rayDir):
            return IntersectPlane(rayOrg, rayDir, self.pos,  self.normal)
    def GenSphereList(sphereDataList):
        lst = []
        for d in sphereDataList:
            s = Sphere(d[0], d[1], d[2])
            lst.append(s)
        return lst
    def GetRayIntersection(rayOrg, rayDir):
        obj = None
        bestDist = MAX_DIST
        for o in sphereList + planeList:
            distance = o.Intersect(rayOrg, rayDir)
            if distance < bestDist:
                bestDist = distance
                obj = o
        return bestDist, obj
    def CastRay(rayOrg, rayDir):
        colourList = []
        deadRay = False
        colour = np.array([0.3,0,0],dtype=np.float32)            
        distance, obj = GetRayIntersection(rayOrg, rayDir)
        if obj != None:
            colour = obj.colour
        return np.array([distance, distance, distance]) / MAX_DIST * 1000
    def RayTracePixel(pixelId):
        px,py = pixelId % screenx, pixelId // screenx
        xAngle = px / screenx - 0.5 * FOV
        yAngle = py / screeny - 0.5 * FOV
        rayDir = np.array([
            xAngle / 45,
            yAngle / 45,
            1.0
        ],dtype=np.float32)
        return CastRay(camPos, rayDir)


    planeList = [Plane([0.0,0.0,0.0], 100, [0,1,1] , [0.0,1.0,0.0])]
    sphereList = GenSphereList(sphereDataList)

    out = np.zeros((screenx, screeny, 3),dtype=np.float32)

    for p in range(pixelStartId, pixelEndId):
        colour = RayTracePixel(p)
        out[p % screenx][p // screenx] = colour

    return out

if __name__ == "__main__":
    '''
    pixelStartId = argList[0]
    pixelEndId = argList[1]
    sphereDataList = argList[2]
    camPos = argList[3]
    screenx = argList[4]
    screeny = argList[5]
    '''
    import numpy as np
    sx,sy = 100,100
    inp = [
        0,
        sx*sy,
        [],
        np.array([0,1,0]),
        sx,
        sy
    ]

    out = func(inp)
    scale = 3
    import pygame
    pygame.init()
    window = pygame.display.set_mode((sx * scale,sy * scale))
    while 1:
        pygame.event.pump()
        for x in range(sx):
            for y in range(sy):
                pygame.draw.rect(window,(out[x][y][0] * 255,out[x][y][1] * 255,out[x][y][2] * 255),(x * scale,y * scale,scale,scale))
        pygame.display.flip()