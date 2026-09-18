"""
Practica 3 - Deteccion de movimiento (equivalente en Python de la app AForge original).

Usa sustraccion de fondo (MOG2) para detectar la region en movimiento mas grande
de cada frame, calcula su centroide y dibuja una estela con el recorrido reciente.
Cada posicion detectada se registra en logs/trayectoria.csv para poder graficarla
despues con graficar_trayectorias.py.

Controles durante la ejecucion:
    s -> guardar una captura de pantalla (para el reporte)
    n -> cambiar el nombre del objeto que se esta probando (limpia la estela)
    q / ESC -> salir
"""

import argparse
import csv
import os
import re
from collections import deque
from datetime import datetime

import cv2

TRAZO_COLOR = (214, 120, 42)  # BGR - azul-naranja de la paleta del laboratorio


def resolve_source(valor):
    """Acepta la ruta a un archivo de video, un indice de camara local ('0', '1', ...)
    o una URL de IP Webcam (ej. 'http://192.168.1.5:8080' o 'http://192.168.1.5:8080/video')."""
    valor = valor.strip()
    if os.path.isfile(valor):
        return valor

    if re.fullmatch(r"\d+", valor):
        return int(valor)

    url = valor if valor.startswith("http") else f"http://{valor}"
    # La app "IP Webcam" expone el stream MJPEG en /video; si el usuario solo
    # da host:puerto, se lo agregamos.
    if not url.rstrip("/").endswith(("/video", ".jpg", ".mjpg", "/videofeed")):
        url = url.rstrip("/") + "/video"
    return url


def elegir_fuente(args, video_prueba_path):
    """Si --source no se especifico, muestra un menu interactivo para elegir entre
    el video de prueba, la webcam local o una IP Webcam."""
    if args.source:
        return resolve_source(args.source)

    print("Selecciona la fuente de video:")
    print(f"  1) Video de prueba ({os.path.basename(video_prueba_path)})")
    print("  2) Webcam local (indice 0)")
    print("  3) IP Webcam (ingresar URL)")
    opcion = input("Opcion [1/2/3] (default 1): ").strip() or "1"

    if opcion == "2":
        return 0
    if opcion == "3":
        url = input("URL de IP Webcam (ej. http://192.168.100.146:8080): ").strip()
        return resolve_source(url)

    if not os.path.isfile(video_prueba_path):
        raise FileNotFoundError(
            f"No se encontro el video de prueba en: {video_prueba_path}\n"
            "Coloca el archivo ahi, o usa --source <ruta/indice/URL> para indicar otra fuente."
        )
    return video_prueba_path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Practica 3 - Deteccion de movimiento con seguimiento de centroide (OpenCV)"
    )
    parser.add_argument(
        "--source", default=None,
        help="Ruta a un video (ej. videos/mosca.mp4), indice de camara local (ej. 0) "
             "o URL de la app IP Webcam (ej. http://192.168.1.5:8080). "
             "Si se omite, se muestra un menu interactivo para elegir.",
    )
    parser.add_argument(
        "--min-area", type=int, default=800,
        help="Area minima en pixeles para considerar una region como objeto en movimiento",
    )
    parser.add_argument(
        "--trail-len", type=int, default=64,
        help="Cantidad de posiciones recientes que se recuerdan para dibujar la estela",
    )
    parser.add_argument(
        "--lost-frames", type=int, default=15,
        help="Frames sin deteccion antes de cortar la estela (evita unir movimientos distintos)",
    )
    parser.add_argument(
        "--mirror", action="store_true",
        help="Aplica efecto espejo (util para webcam frontal; no recomendado con IP Webcam/camara trasera)",
    )
    return parser.parse_args()


def crear_carpetas(base_dir):
    capturas_dir = os.path.join(base_dir, "capturas")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(capturas_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    return capturas_dir, logs_dir


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

    video_prueba_path = os.path.join(base_dir, "videos", "mosca.mp4")
    fuente = elegir_fuente(args, video_prueba_path)
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
    # Con un archivo de video hay que respetar su framerate original; con camara
    # en vivo (local o IP Webcam) conviene el delay minimo para no acumular retraso.
    delay_ms = max(1, int(1000 / fps_video)) if fps_video and fps_video > 0 else 1

    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    sugerencia = "mosca" if es_video_archivo else "objeto_1"
    objeto_actual = input(f"Nombre del objeto a probar (ej. {sugerencia}): ").strip() or sugerencia
    trail = deque(maxlen=args.trail_len)
    frames_sin_deteccion = 0
    frame_idx = 0
    contador_capturas = 0

    print("Controles: [s] guardar captura   [n] cambiar de objeto   [q] salir")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                if es_video_archivo:
                    # Reinicia el video de prueba al llegar al final (loop continuo).
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    trail.clear()
                    continue
                print("No se pudo leer frame de la fuente de video.")
                break

            frame_idx += 1
            if args.mirror:
                frame = cv2.flip(frame, 1)
            blurred = cv2.GaussianBlur(frame, (5, 5), 0)

            fg_mask = bg_subtractor.apply(blurred)
            fg_mask[fg_mask == 127] = 0  # descarta sombras que MOG2 marca como gris
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=1)
            fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

            contornos, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

            for i in range(1, len(trail)):
                cv2.line(frame, trail[i - 1], trail[i], TRAZO_COLOR, 2)

            cv2.putText(
                frame, f"Objeto actual: {objeto_actual}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2,
            )
            cv2.imshow("Practica 3 - Deteccion de movimiento", frame)
            cv2.imshow("Mascara de movimiento (MOG2)", fg_mask)

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
                objeto_actual = input("Nuevo nombre del objeto a probar: ").strip() or objeto_actual
                trail.clear()
                contador_capturas = 0
                print(f"Cambiaste al objeto: {objeto_actual}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        log_file.close()


if __name__ == "__main__":
    main()
