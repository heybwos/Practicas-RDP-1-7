"""
Practica 1 - Deteccion y seguimiento de un objeto por color
(equivalente en Python de la app AForge Color: Deteccion y Seguimiento).

Se hace clic sobre el objeto a seguir; el script toma el color HSV de esa zona
como referencia y sigue esa region por color en cada frame siguiente, dibujando
bounding box, centroide y una estela con el recorrido reciente. Cada posicion
detectada se registra en logs/trayectoria.csv, igual que en la Practica 3, para
poder graficarla despues con graficar_trayectorias.py.

Controles durante la ejecucion:
    clic izquierdo -> selecciona el color del objeto a seguir (muestrea una
                       pequena region alrededor del punto donde haces clic)
    s -> guardar una captura de pantalla (para el reporte)
    n -> cambiar de objeto (pide nuevo nombre y espera un nuevo clic)
    q / ESC -> salir
"""

import argparse
import csv
import os
import re
from collections import deque
from datetime import datetime

import cv2
import numpy as np

TRAZO_COLOR = (214, 120, 42)  # BGR
MUESTRA_RADIO = 8  # px alrededor del clic para muestrear el color de referencia


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


def elegir_fuente(args, videos_prueba):
    """Si --source no se especifico, muestra un menu interactivo para elegir entre
    los videos de prueba disponibles, la webcam local o una IP Webcam.
    videos_prueba: lista de (etiqueta, ruta) con los videos de prueba disponibles."""
    if args.source:
        return resolve_source(args.source)

    print("Selecciona la fuente de video:")
    opciones = {}
    n = 1
    for etiqueta, ruta in videos_prueba:
        print(f"  {n}) {etiqueta} ({os.path.basename(ruta)})")
        opciones[str(n)] = ruta
        n += 1
    idx_webcam = n
    print(f"  {idx_webcam}) Webcam local (indice 0)")
    n += 1
    idx_ipwebcam = n
    print(f"  {idx_ipwebcam}) IP Webcam (ingresar URL)")

    opcion = input(f"Opcion [1-{idx_ipwebcam}] (default 1): ").strip() or "1"

    if opcion == str(idx_webcam):
        return 0
    if opcion == str(idx_ipwebcam):
        url = input("URL de IP Webcam (ej. http://192.168.100.146:8080): ").strip()
        return resolve_source(url)

    video_elegido = opciones.get(opcion, videos_prueba[0][1])
    if not os.path.isfile(video_elegido):
        raise FileNotFoundError(
            f"No se encontro el video de prueba en: {video_elegido}\n"
            "Coloca el archivo ahi, o usa --source <ruta/indice/URL> para indicar otra fuente."
        )
    return video_elegido


def parse_args():
    parser = argparse.ArgumentParser(
        description="Practica 1 - Deteccion y seguimiento de un objeto por color (OpenCV)"
    )
    parser.add_argument(
        "--source", default=None,
        help="Ruta a un video (ej. videos/mosca.mp4), indice de camara local (ej. 0) "
             "o URL de la app IP Webcam (ej. http://192.168.1.5:8080). "
             "Si se omite, se muestra un menu interactivo para elegir.",
    )
    parser.add_argument(
        "--min-area", type=int, default=500,
        help="Area minima en pixeles para considerar una deteccion de color valida",
    )
    parser.add_argument(
        "--trail-len", type=int, default=64,
        help="Cantidad de posiciones recientes que se recuerdan para dibujar la estela",
    )
    parser.add_argument(
        "--lost-frames", type=int, default=15,
        help="Frames sin deteccion antes de cortar la estela",
    )
    parser.add_argument(
        "--mirror", action="store_true",
        help="Aplica efecto espejo (util para webcam frontal; no recomendado con IP Webcam/camara trasera)",
    )
    parser.add_argument("--tol-h", type=int, default=12, help="Tolerancia de matiz (H, 0-179) alrededor del color elegido")
    parser.add_argument("--tol-s", type=int, default=60, help="Tolerancia de saturacion (S, 0-255) alrededor del color elegido")
    parser.add_argument("--tol-v", type=int, default=60, help="Tolerancia de valor/brillo (V, 0-255) alrededor del color elegido")
    return parser.parse_args()


def crear_carpetas(base_dir):
    capturas_dir = os.path.join(base_dir, "capturas")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(capturas_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    return capturas_dir, logs_dir


def muestrear_color(hsv_frame, x, y, radio=MUESTRA_RADIO):
    h, w = hsv_frame.shape[:2]
    x0, x1 = max(0, x - radio), min(w, x + radio)
    y0, y1 = max(0, y - radio), min(h, y + radio)
    region = hsv_frame[y0:y1, x0:x1].reshape(-1, 3)
    return region.mean(axis=0)


def rango_color(color_hsv, tol_h, tol_s, tol_v):
    h, s, v = color_hsv
    lower = np.array([max(0, h - tol_h), max(0, s - tol_s), max(0, v - tol_v)], dtype=np.uint8)
    upper = np.array([min(179, h + tol_h), min(255, s + tol_s), min(255, v + tol_v)], dtype=np.uint8)
    return lower, upper


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    capturas_dir, logs_dir = crear_carpetas(base_dir)

    log_path = os.path.join(logs_dir, "trayectoria.csv")
    log_is_new = not os.path.exists(log_path)
    log_file = open(log_path, "a", newline="", encoding="utf-8")
    log_writer = csv.writer(log_file)
    if log_is_new:
        log_writer.writerow(["timestamp", "objeto", "frame", "cx", "cy", "area"])

    videos_prueba = [
        ("Video de prueba: circulos de colores (varios objetos, colores distintos)", os.path.join(base_dir, "videos", "circulos_colores.mp4")),
        ("Video de prueba: dots (punto rojo en movimiento)", os.path.join(base_dir, "videos", "dots.mp4")),
        ("Video de prueba: mosca (insecto oscuro en movimiento)", os.path.join(base_dir, "videos", "mosca.mp4")),
    ]
    fuente = elegir_fuente(args, videos_prueba)
    cap = cv2.VideoCapture(fuente)
    if not cap.isOpened():
        log_file.close()
        raise RuntimeError(
            f"No se pudo abrir la fuente de video: {fuente}\n"
            "Si es IP Webcam: revisa que el celular y la PC esten en la misma red WiFi, "
            "que la app este mostrando 'Iniciar servidor' activo, y que la URL incluya /video "
            "(ej. http://192.168.1.5:8080/video)."
        )

    es_video_archivo = isinstance(fuente, str) and os.path.isfile(fuente)
    fps_video = cap.get(cv2.CAP_PROP_FPS) if es_video_archivo else 0
    delay_ms = max(1, int(1000 / fps_video)) if fps_video and fps_video > 0 else 1

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    objeto_actual = input("Nombre del objeto a seguir (ej. pelota_roja): ").strip() or "objeto_1"
    trail = deque(maxlen=args.trail_len)
    frames_sin_deteccion = 0
    frame_idx = 0
    contador_capturas = 0
    color_hsv = None  # se define con el primer clic

    ventana = "Practica 1 - Deteccion y seguimiento por color"
    cv2.namedWindow(ventana)

    click_pendiente = {"pos": None}

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            click_pendiente["pos"] = (x, y)

    cv2.setMouseCallback(ventana, on_mouse)

    print("Haz clic sobre el objeto que quieres seguir.")
    print("Controles: [s] guardar captura   [n] cambiar de objeto   [q] salir")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                if es_video_archivo:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    trail.clear()
                    continue
                print("No se pudo leer frame de la fuente de video.")
                break

            frame_idx += 1
            if args.mirror:
                frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            if click_pendiente["pos"] is not None:
                x, y = click_pendiente["pos"]
                click_pendiente["pos"] = None
                color_hsv = muestrear_color(hsv, x, y)
                trail.clear()
                frames_sin_deteccion = 0
                print(f"Color de referencia tomado en ({x},{y}): HSV={color_hsv.round(1).tolist()}")

            if color_hsv is None:
                cv2.putText(
                    frame, "Haz clic sobre el objeto a seguir", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2,
                )
            else:
                lower, upper = rango_color(color_hsv, args.tol_h, args.tol_s, args.tol_v)
                mask = cv2.inRange(hsv, lower, upper)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
                mask = cv2.dilate(mask, kernel, iterations=2)

                contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contorno_principal = None
                if contornos:
                    mayor = max(contornos, key=cv2.contourArea)
                    if cv2.contourArea(mayor) >= args.min_area:
                        contorno_principal = mayor

                if contorno_principal is not None:
                    x, y, w, h = cv2.boundingRect(contorno_principal)
                    momentos = cv2.moments(contorno_principal)
                    cx = int(momentos["m10"] / momentos["m00"])
                    cy = int(momentos["m01"] / momentos["m00"])
                    area = cv2.contourArea(contorno_principal)

                    trail.append((cx, cy))
                    frames_sin_deteccion = 0

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(
                        frame, f"{objeto_actual} ({cx},{cy})", (x, max(y - 10, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2,
                    )

                    log_writer.writerow([
                        datetime.now().isoformat(timespec="seconds"),
                        objeto_actual, frame_idx, cx, cy, f"{area:.0f}",
                    ])
                else:
                    frames_sin_deteccion += 1
                    if frames_sin_deteccion > args.lost_frames:
                        trail.clear()

                cv2.imshow("Mascara de color", mask)

            for i in range(1, len(trail)):
                cv2.line(frame, trail[i - 1], trail[i], TRAZO_COLOR, 2)

            cv2.putText(
                frame, f"Objeto actual: {objeto_actual}", (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2,
            )
            cv2.imshow(ventana, frame)

            key = cv2.waitKey(delay_ms) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("s"):
                contador_capturas += 1
                nombre = f"{objeto_actual}_{contador_capturas}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                ruta = os.path.join(capturas_dir, nombre)
                cv2.imwrite(ruta, frame)
                print(f"Captura guardada: {ruta}")
            elif key == ord("n"):
                objeto_actual = input("Nuevo nombre del objeto a seguir: ").strip() or objeto_actual
                trail.clear()
                contador_capturas = 0
                color_hsv = None
                print(f"Cambiaste al objeto: {objeto_actual}. Haz clic sobre el para recalibrar el color.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        log_file.close()


if __name__ == "__main__":
    main()
