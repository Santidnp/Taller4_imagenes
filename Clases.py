import cv2
import numpy as np
import random

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
        print(self.img.shape)
        cv2.imshow("Fondo",self.img)
        cv2.waitKey(0)


    def generate(self):
        #Magenta (255,0,255)
        Lados = int(np.random.uniform(3, 8, 1))
        Poligono = [[random.randrange(1,512, 1) for col in range(2)] for row in range(Lados)]

        Poligono = np.array([Poligono],np.int32)

        print(Lados)

        img_mod =  cv2.polylines(self.img, [Poligono], True, (255,0,255), thickness=3)
        cv2.imshow('Shapes', img_mod)
        cv2.waitKey(0)
        print(Poligono)


#print(int(np.random.uniform(3,11,1)))

a = Quadrilateral(512)
a.generate()
#
# n = 100
# col1 = np.arange(3,3*n,3)
# col2 = np.arange(1,n)
# matrix = np.hstack((col1.reshape(n-1,1), col2.reshape(n-1,1)))
#
# z = np.array([[[40,160],[120,100],[200,160],[160,240],[80,240]]], np.int32)
# triangle = np.array([[[240, 130], [380, 230], [190, 280]]], np.int32)
#
# print(matrix.shape)
#
# print(z.shape)
#
#
# print(triangle.shape)
# a = [1,2]
#
# b = [[]]
#
# c = b.append(a)
# print(c)