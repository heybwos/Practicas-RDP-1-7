"""
Practica 2 - Modificacion de parametros de imagen: brillo, contraste y saturacion
(equivalente en Python de la app AFORGE Parametro Imagen original).

Carga una imagen (de prueba incluida, de un archivo propio, o una foto tomada con
camara/IP Webcam) y permite ajustar brillo, contraste y saturacion en vivo con
barras deslizantes, mostrando la imagen original y la modificada lado a lado.

Controles:
    s -> guardar (original + modificada) en capturas/ y registrar los parametros
         usados en logs/parametros.csv
    n -> cargar la siguiente imagen (si hay varias) o pedir una nueva
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

VENTANA = "Practica 2 - Parametros de imagen"


def resolve_source(valor):
    """Acepta un indice de camara local ('0', '1', ...) o una URL de IP Webcam
    (ej. 'http://192.168.1.5:8080' o 'http://192.168.1.5:8080/video')."""
    valor = valor.strip()
    if re.fullmatch(r"\d+", valor):
        return int(valor)
    url = valor if valor.startswith("http") else f"http://{valor}"
    if not url.rstrip("/").endswith(("/video", ".jpg", ".mjpg", "/videofeed")):
        url = url.rstrip("/") + "/video"
    return url


def parse_args():
    parser = argparse.ArgumentParser(
        description="Practica 2 - Ajuste de brillo/contraste/saturacion de imagenes (OpenCV)"
    )
    parser.add_argument(
        "--imagen", action="append", default=None,
        help="Ruta a una imagen a usar (se puede repetir la bandera para varias imagenes). "
             "Si se omite, se muestra un menu interactivo.",
    )
    parser.add_argument(
        "--camara-source", default="0",
        help="Fuente de camara para la opcion de captura en vivo: indice local o URL de IP Webcam",
    )
    return parser.parse_args()


def crear_carpetas(base_dir):
    capturas_dir = os.path.join(base_dir, "capturas")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(capturas_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    return capturas_dir, logs_dir


def imagenes_prueba(base_dir):
    carpeta = os.path.join(base_dir, "imagenes")
    rutas = sorted(glob.glob(os.path.join(carpeta, "prueba_*.png")))
    if not rutas:
        raise FileNotFoundError(
            f"No hay imagenes de prueba en {carpeta}.\n"
            "Ejecuta primero: python generar_imagenes_prueba.py"
        )
    return rutas


def capturar_foto(source_str):
    fuente = resolve_source(source_str)
    cap = cv2.VideoCapture(fuente)
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente de camara: {fuente}")

    print("Se abrio la camara. Presiona ESPACIO para capturar la foto, ESC para cancelar.")
    img = None
    ventana_captura = "Captura - ESPACIO para tomar foto, ESC para cancelar"
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("No se pudo leer frame de la camara.")
                break
            cv2.imshow(ventana_captura, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # espacio
                img = frame.copy()
                break
            if key == 27:  # ESC
                break
    finally:
        cap.release()
        cv2.destroyWindow(ventana_captura)
    return img


def elegir_imagenes(args, base_dir):
    if args.imagen:
        rutas = []
        for ruta in args.imagen:
            img = cv2.imread(ruta)
            if img is None:
                raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")
            rutas.append((img, os.path.basename(ruta)))
        return rutas

    print("Selecciona el origen de la(s) imagen(es):")
    print("  1) Imagenes de prueba incluidas")
    print("  2) Ruta a un archivo de imagen propio")
    print("  3) Capturar una foto con camara (webcam o IP Webcam)")
    opcion = input("Opcion [1/2/3] (default 1): ").strip() or "1"

    if opcion == "2":
        ruta = input("Ruta de la imagen: ").strip()
        img = cv2.imread(ruta)
        if img is None:
            raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")
        return [(img, os.path.basename(ruta))]

    if opcion == "3":
        source_str = input(
            "Fuente de camara [indice local (ej. 0) o URL de IP Webcam] "
            "(default 0): "
        ).strip() or "0"
        img = capturar_foto(source_str)
        if img is None:
            raise RuntimeError("No se capturo ninguna foto.")
        nombre = f"captura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        return [(img, nombre)]

    rutas = imagenes_prueba(base_dir)
    return [(cv2.imread(r), os.path.basename(r)) for r in rutas]


def aplicar_parametros(img, brillo, contraste, saturacion):
    """brillo: -100..100 (offset aditivo). contraste: 0.0..3.0 (multiplicador).
    saturacion: 0.0..3.0 (multiplicador sobre el canal S en HSV)."""
    ajustada = cv2.convertScaleAbs(img, alpha=contraste, beta=brillo)
    hsv = cv2.cvtColor(ajustada, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * saturacion, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def combinar_lado_a_lado(original, modificada, alto_max=480):
    def redimensionar(img):
        h, w = img.shape[:2]
        if h <= alto_max:
            return img
        escala = alto_max / h
        return cv2.resize(img, (int(w * escala), alto_max))

    original_r = redimensionar(original)
    modificada_r = redimensionar(modificada)
    separador = np.full((original_r.shape[0], 4, 3), 255, dtype=np.uint8)
    return np.hstack([original_r, separador, modificada_r])


def noop(_valor):
    pass


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    capturas_dir, logs_dir = crear_carpetas(base_dir)

    log_path = os.path.join(logs_dir, "parametros.csv")
    log_is_new = not os.path.exists(log_path)
    log_file = open(log_path, "a", newline="", encoding="utf-8")
    log_writer = csv.writer(log_file)
    if log_is_new:
        log_writer.writerow(["timestamp", "imagen", "brillo", "contraste", "saturacion", "archivo_original", "archivo_modificada"])

    imagenes = elegir_imagenes(args, base_dir)
    indice = 0
    contador_capturas = 0

    cv2.namedWindow(VENTANA)
    cv2.createTrackbar("Brillo", VENTANA, 100, 200, noop)       # -100..+100
    cv2.createTrackbar("Contraste x100", VENTANA, 100, 300, noop)  # 0.00..3.00
    cv2.createTrackbar("Saturacion x100", VENTANA, 100, 300, noop)  # 0.00..3.00

    print("Controles: [s] guardar captura + parametros   [n] siguiente imagen   [q] salir")

    try:
        while True:
            original, nombre = imagenes[indice]

            brillo = cv2.getTrackbarPos("Brillo", VENTANA) - 100
            contraste = cv2.getTrackbarPos("Contraste x100", VENTANA) / 100.0
            saturacion = cv2.getTrackbarPos("Saturacion x100", VENTANA) / 100.0

            modificada = aplicar_parametros(original, brillo, contraste, saturacion)
            combinada = combinar_lado_a_lado(original, modificada)

            cv2.putText(
                combinada, f"{nombre}  |  brillo={brillo}  contraste={contraste:.2f}  saturacion={saturacion:.2f}",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2,
            )
            cv2.putText(
                combinada, f"{nombre}  |  brillo={brillo}  contraste={contraste:.2f}  saturacion={saturacion:.2f}",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
            )
            cv2.imshow(VENTANA, combinada)

            key = cv2.waitKey(30) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("s"):
                contador_capturas += 1
                base_nombre = os.path.splitext(nombre)[0]
                sello = datetime.now().strftime("%Y%m%d_%H%M%S")
                archivo_original = f"{base_nombre}_original_{contador_capturas}_{sello}.png"
                archivo_modificada = f"{base_nombre}_modificada_{contador_capturas}_{sello}.png"
                cv2.imwrite(os.path.join(capturas_dir, archivo_original), original)
                cv2.imwrite(os.path.join(capturas_dir, archivo_modificada), modificada)
                log_writer.writerow([
                    datetime.now().isoformat(timespec="seconds"), nombre,
                    brillo, f"{contraste:.2f}", f"{saturacion:.2f}",
                    archivo_original, archivo_modificada,
                ])
                log_file.flush()
                print(f"Captura guardada: {archivo_original} / {archivo_modificada}")
            elif key == ord("n"):
                indice = (indice + 1) % len(imagenes)
                print(f"Imagen actual: {imagenes[indice][1]}")
    finally:
        cv2.destroyAllWindows()
        log_file.close()


if __name__ == "__main__":
    main()
