"""
Practica 6 - Lector de codigos de barras (equivalente en Python de la app AFORGE
Lector Bar Code original).

Lee y decodifica codigos de barras (y QR) en una imagen o en video de camara en
tiempo real usando pyzbar (bindings de ZBar), y muestra/registra la secuencia
numerica/alfanumerica decodificada.

Controles:
    s -> guardar captura de pantalla (con el codigo y su valor etiquetados)
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
from pyzbar.pyzbar import decode


def resolve_source(valor):
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
    parser = argparse.ArgumentParser(description="Practica 6 - Lector de codigos de barras (pyzbar + OpenCV)")
    parser.add_argument(
        "--source", default=None,
        help="Ruta a una imagen/video, indice de camara local (ej. 0), o URL de "
             "IP Webcam. Si se omite, se muestra un menu interactivo.",
    )
    parser.add_argument("--mirror", action="store_true", help="Aplica efecto espejo (webcam frontal)")
    return parser.parse_args()


def crear_carpetas(base_dir):
    capturas_dir = os.path.join(base_dir, "capturas")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(capturas_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    return capturas_dir, logs_dir


def imagenes_prueba(base_dir):
    carpeta = os.path.join(base_dir, "imagenes")
    rutas = sorted(glob.glob(os.path.join(carpeta, "codigo_*.png")))
    if not rutas:
        raise FileNotFoundError(
            f"No hay codigos de prueba en {carpeta}.\nEjecuta primero: python generar_codigos_prueba.py"
        )
    return rutas


def elegir_fuente(args, base_dir):
    if args.source:
        return resolve_source(args.source)

    print("Selecciona la fuente:")
    print("  1) Codigos de barras de prueba incluidos")
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

    return imagenes_prueba(base_dir)


def leer_codigos(frame):
    resultados = decode(frame)
    codigos = []
    for r in resultados:
        try:
            dato = r.data.decode("utf-8")
        except UnicodeDecodeError:
            dato = repr(r.data)
        codigos.append({"tipo": r.type, "dato": dato, "rect": r.rect})
    return codigos


def dibujar_codigos(frame, codigos):
    for c in codigos:
        x, y, w, h = c["rect"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        etiqueta = f"{c['tipo']}: {c['dato']}"
        cv2.putText(frame, etiqueta, (x, max(y - 10, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    return frame


def modo_imagenes(rutas, capturas_dir, log_writer, log_file):
    indice = 0
    contador_capturas = 0
    print("Controles: [s] guardar captura   [n] siguiente imagen   [q] salir")
    while True:
        ruta = rutas[indice]
        original = cv2.imread(ruta)
        if original is None:
            raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")

        frame = original.copy()
        codigos = leer_codigos(frame)
        dibujar_codigos(frame, codigos)
        cv2.putText(frame, os.path.basename(ruta), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        if not codigos:
            cv2.putText(frame, "Sin codigo detectado", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

        cv2.imshow("Practica 6 - Lector de codigos de barras", frame)
        key = cv2.waitKey(30) & 0xFF
        if key in (ord("q"), 27):
            break
        elif key == ord("n"):
            indice = (indice + 1) % len(rutas)
        elif key == ord("s"):
            contador_capturas += 1
            nombre_archivo = f"{os.path.splitext(os.path.basename(ruta))[0]}_{contador_capturas}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(os.path.join(capturas_dir, nombre_archivo), frame)
            for c in codigos:
                log_writer.writerow([datetime.now().isoformat(timespec="seconds"), os.path.basename(ruta), c["tipo"], c["dato"]])
            log_file.flush()
            print(f"Captura guardada: {nombre_archivo} ({len(codigos)} codigo(s) detectado(s))")


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

            codigos = leer_codigos(frame)
            dibujar_codigos(frame, codigos)
            cv2.imshow("Practica 6 - Lector de codigos de barras", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("s"):
                contador_capturas += 1
                nombre_archivo = f"webcam_{contador_capturas}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                cv2.imwrite(os.path.join(capturas_dir, nombre_archivo), frame)
                for c in codigos:
                    log_writer.writerow([datetime.now().isoformat(timespec="seconds"), "webcam", c["tipo"], c["dato"]])
                log_file.flush()
                print(f"Captura guardada: {nombre_archivo} ({len(codigos)} codigo(s) detectado(s))")
    finally:
        cap.release()


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    capturas_dir, logs_dir = crear_carpetas(base_dir)

    log_path = os.path.join(logs_dir, "codigos.csv")
    log_is_new = not os.path.exists(log_path)
    log_file = open(log_path, "a", newline="", encoding="utf-8")
    log_writer = csv.writer(log_file)
    if log_is_new:
        log_writer.writerow(["timestamp", "fuente", "tipo", "dato_decodificado"])

    fuente = elegir_fuente(args, base_dir)

    try:
        if isinstance(fuente, list):
            modo_imagenes(fuente, capturas_dir, log_writer, log_file)
        elif isinstance(fuente, str) and fuente.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            modo_imagenes([fuente], capturas_dir, log_writer, log_file)
        else:
            modo_video(fuente, args, capturas_dir, log_writer, log_file)
    finally:
        cv2.destroyAllWindows()
        log_file.close()


if __name__ == "__main__":
    main()
