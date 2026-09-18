"""
Practica 4 - Deteccion de formas geometricas (equivalente en Python de la app
AFORGE Formas Webcam original).

Detecta figuras basicas (triangulo, cuadrado, rectangulo, pentagono, hexagono,
circulo) en una imagen o en video de camara en tiempo real, usando contornos y
aproximacion poligonal con OpenCV.

Controles:
    s -> guardar captura de pantalla (con las formas ya etiquetadas)
    n -> siguiente imagen de prueba (solo en modo imagenes)
    q / ESC -> salir
"""

import argparse
import csv
import glob
import os
import re
from datetime import datetime

import cv2
import numpy as np

MIN_AREA = 800


def resolve_source(valor):
    """Acepta la ruta a un archivo de video, un indice de camara local ('0', '1', ...)
    o una URL de IP Webcam (ej. 'http://192.168.1.5:8080' o 'http://192.168.1.5:8080/video')."""
    valor = valor.strip()
    if os.path.isfile(valor):
        return valor
    if re.fullmatch(r"\d+", valor):
        return int(valor)
    url = valor if valor.startswith("http") else f"http://{valor}"
    if not url.rstrip("/").endswith(("/video", ".jpg", ".mjpg", "/videofeed")):
        url = url.rstrip("/") + "/video"
    return url


def parse_args():
    parser = argparse.ArgumentParser(
        description="Practica 4 - Deteccion de formas geometricas (OpenCV)"
    )
    parser.add_argument(
        "--source", default=None,
        help="Ruta a una imagen o video, indice de camara local (ej. 0), o URL de "
             "IP Webcam. Si se omite, se muestra un menu interactivo.",
    )
    parser.add_argument("--min-area", type=int, default=MIN_AREA, help="Area minima en pixeles para considerar una figura valida")
    parser.add_argument("--mirror", action="store_true", help="Aplica efecto espejo (webcam frontal)")
    return parser.parse_args()


def crear_carpetas(base_dir):
    capturas_dir = os.path.join(base_dir, "capturas")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(capturas_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    return capturas_dir, logs_dir


def clasificar_forma(contorno, approx):
    vertices = len(approx)
    if vertices == 3:
        return "Triangulo"
    if vertices == 4:
        x, y, w, h = cv2.boundingRect(approx)
        ratio = w / float(h)
        return "Cuadrado" if 0.90 <= ratio <= 1.10 else "Rectangulo"
    if vertices == 5:
        return "Pentagono"
    if vertices == 6:
        return "Hexagono"

    area = cv2.contourArea(contorno)
    perimetro = cv2.arcLength(contorno, True)
    circularidad = 4 * np.pi * area / (perimetro ** 2) if perimetro > 0 else 0
    return "Circulo" if circularidad > 0.75 else f"Poligono({vertices})"


def detectar_formas(frame, min_area):
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)
    umbral_otsu, _ = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bordes = cv2.Canny(blur, umbral_otsu * 0.5, umbral_otsu)
    bordes = cv2.dilate(bordes, None, iterations=1)

    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    formas = []
    for c in contornos:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        perimetro = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
        nombre = clasificar_forma(c, approx)
        momentos = cv2.moments(c)
        if momentos["m00"] == 0:
            continue
        cx = int(momentos["m10"] / momentos["m00"])
        cy = int(momentos["m01"] / momentos["m00"])
        formas.append({"nombre": nombre, "approx": approx, "area": area, "cx": cx, "cy": cy, "vertices": len(approx)})
    return formas


def dibujar_formas(frame, formas):
    for f in formas:
        cv2.drawContours(frame, [f["approx"]], -1, (0, 255, 0), 2)
        cv2.circle(frame, (f["cx"], f["cy"]), 4, (0, 0, 255), -1)
        cv2.putText(
            frame, f["nombre"], (f["cx"] - 40, f["cy"] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2,
        )
    return frame


def imagenes_prueba(base_dir):
    carpeta = os.path.join(base_dir, "imagenes")
    rutas = sorted(glob.glob(os.path.join(carpeta, "formas_*.png")))
    if not rutas:
        raise FileNotFoundError(
            f"No hay imagenes de prueba en {carpeta}.\nEjecuta primero: python generar_imagenes_prueba.py"
        )
    return rutas


def elegir_fuente(args, base_dir):
    if args.source:
        return resolve_source(args.source)

    print("Selecciona la fuente:")
    print("  1) Imagenes de prueba incluidas (formas geometricas)")
    print("  2) Ruta a una imagen propia")
    print("  3) Webcam local (indice 0)")
    print("  4) IP Webcam (ingresar URL)")
    opcion = input("Opcion [1/2/3/4] (default 1): ").strip() or "1"

    if opcion == "2":
        ruta = input("Ruta de la imagen: ").strip()
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"No se encontro la imagen: {ruta}")
        return ruta
    if opcion == "3":
        return 0
    if opcion == "4":
        url = input("URL de IP Webcam (ej. http://192.168.100.146:8080): ").strip()
        return resolve_source(url)

    return imagenes_prueba(base_dir)  # lista de rutas -> modo imagenes


def modo_imagenes(rutas, args, capturas_dir, log_writer, log_file):
    indice = 0
    contador_capturas = 0
    print("Controles: [s] guardar captura   [n] siguiente imagen   [q] salir")
    while True:
        ruta = rutas[indice]
        original = cv2.imread(ruta)
        if original is None:
            raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")

        frame = original.copy()
        formas = detectar_formas(frame, args.min_area)
        dibujar_formas(frame, formas)
        cv2.putText(frame, os.path.basename(ruta), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        cv2.imshow("Practica 4 - Deteccion de formas", frame)
        key = cv2.waitKey(30) & 0xFF
        if key in (ord("q"), 27):
            break
        elif key == ord("n"):
            indice = (indice + 1) % len(rutas)
        elif key == ord("s"):
            contador_capturas += 1
            nombre_archivo = f"{os.path.splitext(os.path.basename(ruta))[0]}_{contador_capturas}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(os.path.join(capturas_dir, nombre_archivo), frame)
            for f in formas:
                log_writer.writerow([
                    datetime.now().isoformat(timespec="seconds"), os.path.basename(ruta),
                    f["nombre"], f["vertices"], f"{f['area']:.0f}", f["cx"], f["cy"],
                ])
            log_file.flush()
            print(f"Captura guardada: {nombre_archivo} ({len(formas)} figura(s) detectada(s))")


def modo_video(fuente, args, capturas_dir, log_writer, log_file):
    cap = cv2.VideoCapture(fuente)
    if not cap.isOpened():
        raise RuntimeError(
            f"No se pudo abrir la fuente de video: {fuente}\n"
            "Si es IP Webcam: revisa que el celular y la PC esten en la misma red WiFi, "
            "que la app este mostrando 'Iniciar servidor' activo, y que la URL incluya /video."
        )

    contador_capturas = 0
    print("Controles: [s] guardar captura   [q] salir")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("No se pudo leer frame de la fuente de video.")
                break
            if args.mirror:
                frame = cv2.flip(frame, 1)

            formas = detectar_formas(frame, args.min_area)
            dibujar_formas(frame, formas)
            cv2.imshow("Practica 4 - Deteccion de formas", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("s"):
                contador_capturas += 1
                nombre_archivo = f"webcam_{contador_capturas}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                cv2.imwrite(os.path.join(capturas_dir, nombre_archivo), frame)
                for f in formas:
                    log_writer.writerow([
                        datetime.now().isoformat(timespec="seconds"), "webcam",
                        f["nombre"], f["vertices"], f"{f['area']:.0f}", f["cx"], f["cy"],
                    ])
                log_file.flush()
                print(f"Captura guardada: {nombre_archivo} ({len(formas)} figura(s) detectada(s))")
    finally:
        cap.release()


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    capturas_dir, logs_dir = crear_carpetas(base_dir)

    log_path = os.path.join(logs_dir, "formas.csv")
    log_is_new = not os.path.exists(log_path)
    log_file = open(log_path, "a", newline="", encoding="utf-8")
    log_writer = csv.writer(log_file)
    if log_is_new:
        log_writer.writerow(["timestamp", "fuente", "forma", "vertices", "area", "cx", "cy"])

    fuente = elegir_fuente(args, base_dir)

    try:
        if isinstance(fuente, list):
            modo_imagenes(fuente, args, capturas_dir, log_writer, log_file)
        elif isinstance(fuente, str) and fuente.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            modo_imagenes([fuente], args, capturas_dir, log_writer, log_file)
        else:
            modo_video(fuente, args, capturas_dir, log_writer, log_file)
    finally:
        cv2.destroyAllWindows()
        log_file.close()


if __name__ == "__main__":
    main()
