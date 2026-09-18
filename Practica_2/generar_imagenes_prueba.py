"""
Genera un par de imagenes de prueba sinteticas (sin depender de internet ni de
archivos externos) para poder probar parametros_imagen.py sin necesidad de
camara. Se guardan en imagenes/prueba_1.png y imagenes/prueba_2.png.

Ejecutar una sola vez (o cuando se quieran regenerar):
    python generar_imagenes_prueba.py
"""

import os

import cv2
import numpy as np


def imagen_prueba_1(w=640, h=480):
    """Fondo degradado + formas de colores solidos, ideal para ver el efecto
    de brillo/contraste/saturacion sobre areas planas de color."""
    img = np.zeros((h, w, 3), dtype=np.uint8)
    for x in range(w):
        t = x / w
        img[:, x] = (int(200 * t + 30), 110, int(200 * (1 - t) + 30))  # BGR

    cv2.circle(img, (160, 240), 90, (40, 40, 220), -1)
    cv2.rectangle(img, (350, 120), (560, 360), (60, 180, 60), -1)
    cv2.ellipse(img, (480, 400), (80, 40), 0, 0, 360, (200, 200, 30), -1)
    cv2.putText(img, "PRUEBA 1", (190, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)
    return img


def imagen_prueba_2(w=640, h=480):
    """Patron tipo tablero con colores alternados, util para notar bien los
    cambios de saturacion y contraste en bordes definidos."""
    img = np.zeros((h, w, 3), dtype=np.uint8)
    tam = 48
    colores = [(180, 60, 60), (60, 170, 230), (200, 60, 200), (70, 200, 90)]
    for j in range(0, h, tam):
        for i in range(0, w, tam):
            color = colores[((i // tam) + (j // tam)) % len(colores)]
            img[j:j + tam, i:i + tam] = color
    cv2.putText(img, "PRUEBA 2", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 255, 255), 4)
    return img


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base_dir, "imagenes")
    os.makedirs(carpeta, exist_ok=True)

    ruta_1 = os.path.join(carpeta, "prueba_1.png")
    ruta_2 = os.path.join(carpeta, "prueba_2.png")
    cv2.imwrite(ruta_1, imagen_prueba_1())
    cv2.imwrite(ruta_2, imagen_prueba_2())
    print(f"Imagenes generadas:\n  {ruta_1}\n  {ruta_2}")


if __name__ == "__main__":
    main()
