"""
Practica 5 - Fotomaton (equivalente en Python de la app AFORGE Fotomaton / "Mis
Fotitos" original).

Toma fotos en secuencia desde la camara (webcam o IP Webcam) y les aplica un
filtro de color y un fondo/marco decorativo, como una cabina fotografica.

Controles:
    ESPACIO -> tomar la foto (aplica el filtro y fondo actuales, la guarda)
    f -> cambiar de filtro de color
    b -> cambiar de fondo/marco
    q / ESC -> salir
"""

import argparse
import csv
import os
import re
from datetime import datetime

import cv2
import numpy as np

FILTROS = ["original", "grises", "sepia", "invertido", "frio", "calido"]

# Fondos en BGR
FONDOS = {
    "blanco": (255, 255, 255),
    "negro": (20, 20, 20),
    "rosa_pastel": (222, 178, 248),
    "azul_pastel": (235, 190, 120),
}
NOMBRES_FONDOS = list(FONDOS.keys())


def resolve_source(valor):
    valor = valor.strip()
    if re.fullmatch(r"\d+", valor):
        return int(valor)
    url = valor if valor.startswith("http") else f"http://{valor}"
    if not url.rstrip("/").endswith(("/video", ".jpg", ".mjpg", "/videofeed")):
        url = url.rstrip("/") + "/video"
    return url


def parse_args():
    parser = argparse.ArgumentParser(description="Practica 5 - Fotomaton (OpenCV)")
    parser.add_argument(
        "--source", default=None,
        help="Indice de camara local (ej. 0) o URL de IP Webcam. Si se omite, se pregunta.",
    )
    parser.add_argument("--mirror", action="store_true", default=None, help="Fuerza efecto espejo")
    return parser.parse_args()


def crear_carpetas(base_dir):
    capturas_dir = os.path.join(base_dir, "capturas")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(capturas_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    return capturas_dir, logs_dir


def elegir_fuente(args):
    if args.source:
        return resolve_source(args.source), (args.mirror if args.mirror is not None else True)

    print("Selecciona la camara:")
    print("  1) Webcam local (indice 0)")
    print("  2) IP Webcam (ingresar URL)")
    opcion = input("Opcion [1/2] (default 1): ").strip() or "1"
    if opcion == "2":
        url = input("URL de IP Webcam (ej. http://192.168.100.146:8080): ").strip()
        return resolve_source(url), False
    return 0, True


def aplicar_filtro(img, nombre):
    if nombre == "grises":
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
    if nombre == "sepia":
        kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189],
        ])
        sepia = cv2.transform(img, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)
    if nombre == "invertido":
        return cv2.bitwise_not(img)
    if nombre == "frio":
        b, g, r = cv2.split(img.astype(np.int16))
        b = np.clip(b + 25, 0, 255)
        r = np.clip(r - 15, 0, 255)
        return cv2.merge([b, g, r]).astype(np.uint8)
    if nombre == "calido":
        b, g, r = cv2.split(img.astype(np.int16))
        r = np.clip(r + 25, 0, 255)
        b = np.clip(b - 15, 0, 255)
        return cv2.merge([b, g, r]).astype(np.uint8)
    return img  # original


def aplicar_fondo(foto, nombre_fondo, margen=40):
    color = FONDOS[nombre_fondo]
    h, w = foto.shape[:2]
    lienzo = np.full((h + 2 * margen, w + 2 * margen, 3), color, dtype=np.uint8)
    lienzo[margen:margen + h, margen:margen + w] = foto

    brillo = sum(color) / 3
    color_texto = (0, 0, 0) if brillo > 140 else (255, 255, 255)
    cv2.putText(
        lienzo, "FOTOMATON - Practica 5", (margen, margen - 12),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_texto, 2,
    )
    return lienzo


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    capturas_dir, logs_dir = crear_carpetas(base_dir)

    log_path = os.path.join(logs_dir, "fotomaton.csv")
    log_is_new = not os.path.exists(log_path)
    log_file = open(log_path, "a", newline="", encoding="utf-8")
    log_writer = csv.writer(log_file)
    if log_is_new:
        log_writer.writerow(["timestamp", "filtro", "fondo", "archivo"])

    fuente, mirror_default = elegir_fuente(args)
    mirror = args.mirror if args.mirror is not None else mirror_default

    cap = cv2.VideoCapture(fuente)
    if not cap.isOpened():
        log_file.close()
        raise RuntimeError(
            f"No se pudo abrir la fuente de video: {fuente}\n"
            "Si es IP Webcam: revisa que el celular y la PC esten en la misma red WiFi, "
            "que la app este mostrando 'Iniciar servidor' activo, y que la URL incluya /video."
        )

    indice_filtro = 0
    indice_fondo = 0
    contador_capturas = 0

    print("Controles: [ESPACIO] tomar foto   [f] cambiar filtro   [b] cambiar fondo   [q] salir")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("No se pudo leer frame de la camara.")
                break
            if mirror:
                frame = cv2.flip(frame, 1)

            filtro = FILTROS[indice_filtro]
            fondo = NOMBRES_FONDOS[indice_fondo]
            vista_previa = aplicar_filtro(frame, filtro)

            cv2.putText(
                vista_previa, f"Filtro: {filtro}  |  Fondo: {fondo}  |  [ESPACIO] foto  [f] filtro  [b] fondo",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2,
            )
            cv2.imshow("Practica 5 - Fotomaton", vista_previa)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("f"):
                indice_filtro = (indice_filtro + 1) % len(FILTROS)
            elif key == ord("b"):
                indice_fondo = (indice_fondo + 1) % len(NOMBRES_FONDOS)
            elif key == 32:  # espacio
                foto_filtrada = aplicar_filtro(frame, filtro)
                foto_final = aplicar_fondo(foto_filtrada, fondo)
                contador_capturas += 1
                nombre_archivo = f"foto_{contador_capturas}_{filtro}_{fondo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                ruta = os.path.join(capturas_dir, nombre_archivo)
                cv2.imwrite(ruta, foto_final)
                log_writer.writerow([datetime.now().isoformat(timespec="seconds"), filtro, fondo, nombre_archivo])
                log_file.flush()
                print(f"Foto guardada: {nombre_archivo}")

                # Pequeno "flash" de confirmacion visual
                flash = np.full_like(vista_previa, 255)
                cv2.imshow("Practica 5 - Fotomaton", flash)
                cv2.waitKey(80)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        log_file.close()


if __name__ == "__main__":
    main()
