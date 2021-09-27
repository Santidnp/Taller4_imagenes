import cv2
import numpy as np

class Quadrilateral:

    def __init__(self,N):

        self.N = N
        if N%2 != 0:
            raise ValueError('N solo puede número  par')
        #cyan = (255 255 0)

        img = np.zeros((N,N,3))
        b, g, r = cv2.split(img)
        b += 255
        g += 255
        img = cv2.merge([b, g, r])
        print(img.shape)
        cv2.imshow("Fondo",img)
        cv2.waitKey(0)


    def generate(self):
        Lados = int(np.random.uniform(3, 11, 1))
        pass


print(int(np.random.uniform(3,11,1)))

a = Quadrilateral(512)

n = 100
col1 = np.arange(3,3*n,3)
col2 = np.arange(1,n)
matrix = np.hstack((col1.reshape(n-1,1), col2.reshape(n-1,1)))

z = np.array([[[40,160],[120,100],[200,160],[160,240],[80,240]]], np.int32)
triangle = np.array([[[240, 130], [380, 230], [190, 280]]], np.int32)

print(matrix.shape)

print(z.shape)


print(triangle.shape)
a = [1,2]

b = [[]]

c = b.append(a)
print(c)