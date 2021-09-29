"""
Autores: Laura Juliana Ramos Maldonado, Santiago Nicolás García Herrera
"""
# Cargar librerias

import cv2
import numpy as np
import random
import math
import sys
from enum import Enum
from hough import Hough
from gradient_map import gradient_map




class Methods(Enum):
    # Creación clase metodos
    Standard = 1
    Direct = 2

class Quadrilateral:

    # Creación de la clase principal en la que se crea el poligono y posteriormente se encuentran sus esquinas


    def __init__(self,N):

        # Se genera una imagen de fondo cyan

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

        """
        Se generá puntos aleatorios de un circulo para formar los poligonos

        """
        self.Lados = int(np.random.uniform(3, 8, 1))

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

        Poligono= generatePolygon(ctrX=self.N/2, ctrY=self.N/2, aveRadius=int(np.random.uniform(self.N*0.2,self.N/2, 1)), irregularity=0.35, spikeyness=0.2, numVerts=self.Lados)
        Poligono = np.array([Poligono],np.int32)
        #print(Lados)
        self.img_mod = cv2.fillPoly(self.img, [Poligono], (255, 0, 255))
        print(type(self.img_mod))
        cv2.imshow('Shapes', self.img_mod)
        cv2.waitKey(0)
        cv2.imwrite("poligono.jpeg",self.img_mod)
       # print(Poligono)

    def DetectCorners(self):
        """
        Retorna las esquinas del poligono



        """
        path = "poligono.jpeg" # Cargar imagen del poligono creado anteriormente
        image = cv2.imread(path)

        high_thresh = 300
        method = Methods.Standard
        bw_edges = cv2.Canny(image, high_thresh * 0.3, high_thresh, L2gradient=True) # Detectar contorno de la imagen
        hough = Hough(bw_edges)

        if method == Methods.Standard:
            accumulator = hough.standard_transform()
        elif method == Methods.Direct:
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            theta, _ = gradient_map(image_gray)
            accumulator = hough.direct_transform(theta)
        else:
            sys.exit()

        acc_thresh = 50
        N_peaks = 11
        nhood = [25, 9]
        peaks = hough.find_peaks(accumulator, nhood, acc_thresh, N_peaks)

        _, cols = image.shape[:2]
        image_draw = np.copy(image)

        Puntos_Rectas = []

        for peak in peaks:
            # si la línea pasa por debajo del origen, tendrá un rho positivo y un ángulo menor de 180
            rho = peak[0]
            theta_ = hough.theta[peak[1]]

            theta_pi = np.pi * theta_ / 180
            theta_ = theta_ - 180
            a = np.cos(theta_pi)
            b = np.sin(theta_pi)
            x0 = a * rho + hough.center_x
            y0 = b * rho + hough.center_y
            c = -rho
            x1 = int(round(x0 + cols * (-b)))
            y1 = int(round(y0 + cols * a))
            x2 = int(round(x0 - cols * (-b)))
            y2 = int(round(y0 - cols * a))
            #print("recta:")
            #print("x1", x1, "y1", y1)
            #print("x2", x2, "y2", y2)
            Puntos_Rectas.append([[x1,y1],[x2,y2]])



            # Dibujar lineas del poligono
            if np.abs(theta_) < 80:
                image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)
            elif np.abs(theta_) > 100:
                image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)
            else:
                if theta_ > 0:
                    image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)
                else:
                    image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)


        def line_intersection(line1, line2):
            """
            Calcular punto de intersección entre 2 rectas

            """
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                raise Exception('lines do not intersect')

            d = (det(*line1), det(*line2))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            return x, y

        cv2.imshow("bordes", bw_edges)
        #print(bw_edges)
        #print(Puntos_Rectas)
        #print(Puntos_Rectas[0])
        #print(Puntos_Rectas[1])
        #print(Puntos_Rectas[0][1])
        #contador = 0
        for i in range(self.Lados):
            for j in range(i+1,self.Lados):
                x_in, y_in = line_intersection(Puntos_Rectas[i], Puntos_Rectas[j])
            #x_in, y_in = line_intersection(Puntos_Rectas[i], Puntos_Rectas[i+2])
                cv2.circle(image_draw, (int(x_in), int(y_in)),5, (0, 255, 255), 5)


        #x_in, y_in =line_intersection(Puntos_Rectas[1], Puntos_Rectas[2])
        #x_in1, y_in2 = line_intersection(Puntos_Rectas[0], Puntos_Rectas[1])
        #print(x_in, y_in)
        #cv2.circle(image_draw, (int(x_in), int(y_in)), 5, (0, 255, 255), 5)
        #cv2.circle(image_draw, (int(x_in1), int(y_in2)), 5, (0, 255, 255), 5)
        cv2.imshow("lineas", image_draw)
        cv2.waitKey(0)










