import os
import sys
from enum import Enum
import numpy as np
from _7_lines_detection.hough import Hough
from _6_edges_and_orientation.orientation_methods import gradient_map
import cv2

""" Straight lines detection

    python find_lines.py <path_to_image> <image_name> 
"""

class Methods(Enum):
    Standard = 1
    Direct = 2

if __name__ == '__main__':
    #path = sys.argv[1]
    #image_name = sys.argv[2]
    #path_file = os.path.join(path, image_name)
    path_file=r'C:\Users\Laura\Desktop\Procesamiento imagenes\taller4\Taller4_imagenes\poligono.jpeg'
    image = cv2.imread(path_file)
    cv2.imshow('imagen',image)
    cv2.waitKey(0)

    method = Methods.Standard
    high_thresh = 300
    bw_edges = cv2.Canny(image, high_thresh * 0.3, high_thresh, L2gradient=True)
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

    for peak in peaks:
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
        print("recta:")
        print("x1", x1, "y1", y1)
        print("x2", x2, "y2", y2)

        if np.abs(theta_) < 80:
            image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 255, 255], thickness=2)
        elif np.abs(theta_) > 100:
            image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [255, 0, 255], thickness=2)
        else:
            if theta_ > 0:
                image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 255, 0], thickness=2)
            else:
                image_draw = cv2.line(image_draw, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)

    cv2.imshow("bordes", bw_edges)
    cv2.imshow("lineas", image_draw)
    cv2.waitKey(0)
