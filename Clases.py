import cv2
import numpy as np
import random
import math

class Quadrilateral:


    def __init__(self,N):

        self.N = N
        if N%2 != 0:
            raise ValueError('N solo puede número  par')
        #cyan = (255 255 0)

        self.img = np.zeros((N,N,3))
        b, g, r = cv2.split(self.img)
        b += 255
        g += 255
        self.img = cv2.merge([b, g, r])
        #print(self.img.shape)
        #cv2.imshow("Fondo",self.img)
        #cv2.waitKey(0)


    def generate(self):
        Lados = int(np.random.uniform(3, 8, 1))

        def clip(x, min, max):
            if (min > max):
                return x
            elif (x < min):
                return min
            elif (x > max):
                return max
            else:
                return x

        def generatePolygon(ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts):

            irregularity = clip(irregularity, 0, 1) * 2 * math.pi / numVerts
            spikeyness = clip(spikeyness, 0, 1) * aveRadius


            angleSteps = []
            lower = (2 * math.pi / numVerts) - irregularity
            upper = (2 * math.pi / numVerts) + irregularity
            sum = 0
            for i in range(numVerts):
                tmp = random.uniform(lower, upper)
                angleSteps.append(tmp)
                sum = sum + tmp


            k = sum / (2 * math.pi)
            for i in range(numVerts):
                angleSteps[i] = angleSteps[i] / k

            # now generate the points
            points = []
            angle = random.uniform(0, 2 * math.pi)
            for i in range(numVerts):
                r_i = clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
                x = ctrX + r_i * math.cos(angle)
                y = ctrY + r_i * math.sin(angle)
                points.append([int(x), int(y)])

                angle = angle + angleSteps[i]

            return points

        Poligono= generatePolygon(ctrX=self.N/2, ctrY=self.N/2, aveRadius=int(np.random.uniform(self.N*0.1, np.sqrt(2*(self.N)**2)/2-self.N*0.1, 1)), irregularity=0.35, spikeyness=0.2, numVerts=Lados)



        Poligono = np.array([Poligono],np.int32)

        #print(Lados)

        img_mod =  cv2.polylines(self.img, [Poligono], True, (255,0,255), thickness=3)
        cv2.imshow('Shapes', img_mod)
        cv2.waitKey(0)
        print(Poligono)


#print(int(np.random.uniform(3,11,1)))

a = Quadrilateral(512)
a.generate()




