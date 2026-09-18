"""
Genera dos imagenes de prueba con figuras geometricas basicas (sin depender de
internet) para probar deteccion_formas.py sin necesidad de camara. Se guardan en
imagenes/formas_1.png e imagenes/formas_2.png.

Ejecutar una sola vez (o cuando se quieran regenerar):
    python generar_imagenes_prueba.py
"""

import os

import cv2
import numpy as np


def imagen_formas_1(w=640, h=480):
    img = np.full((h, w, 3), 255, dtype=np.uint8)
    cv2.rectangle(img, (40, 60), (180, 200), (60, 60, 60), -1)           # cuadrado (140x140)
    cv2.rectangle(img, (250, 60), (500, 180), (60, 60, 60), -1)          # rectangulo
    cv2.circle(img, (130, 340), 90, (60, 60, 60), -1)                    # circulo
    triangulo = np.array([[380, 420], [480, 250], [580, 420]], np.int32)
    cv2.fillPoly(img, [triangulo], (60, 60, 60))                        # triangulo
    return img


def imagen_formas_2(w=640, h=480):
    img = np.full((h, w, 3), 255, dtype=np.uint8)

    def poligono_regular(centro, radio, n_lados, angulo0=-90):
        pts = []
        for k in range(n_lados):
            ang = np.deg2rad(angulo0 + k * 360 / n_lados)
            pts.append((int(centro[0] + radio * np.cos(ang)), int(centro[1] + radio * np.sin(ang))))
        return np.array(pts, np.int32)

    cv2.fillPoly(img, [poligono_regular((150, 150), 100, 5)], (60, 60, 60))   # pentagono
    cv2.fillPoly(img, [poligono_regular((470, 150), 100, 6)], (60, 60, 60))   # hexagono
    cv2.circle(img, (150, 370), 85, (60, 60, 60), -1)                          # circulo
    cv2.rectangle(img, (390, 290), (560, 430), (60, 60, 60), -1)               # cuadrado
    return img


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base_dir, "imagenes")
    os.makedirs(carpeta, exist_ok=True)

    ruta_1 = os.path.join(carpeta, "formas_1.png")
    ruta_2 = os.path.join(carpeta, "formas_2.png")
    cv2.imwrite(ruta_1, imagen_formas_1())
    cv2.imwrite(ruta_2, imagen_formas_2())
    print(f"Imagenes generadas:\n  {ruta_1}\n  {ruta_2}")


if __name__ == "__main__":
    main()
