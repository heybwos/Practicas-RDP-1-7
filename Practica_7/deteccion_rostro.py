"""
Practica 7 - Deteccion de rostros (equivalente en Python de la app AFORGE
Movimiento Rostro original).

Detecta rostros en una fotografia o en video de camara en tiempo real usando el
detector YuNet (red neuronal ligera, formato ONNX) incluido en el modulo DNN de
OpenCV. Nota: OpenCV 5.x elimino el clasificador clasico basado en Haar Cascades
(cv2.CascadeClassifier ya no existe en este build); YuNet es el reemplazo oficial
recomendado por el propio proyecto OpenCV.

Controles:
    s -> guardar captura de pantalla (con los rostros etiquetados)
    n -> siguiente imagen (solo en modo imagenes)
    q / ESC -> salir
"""

import argparse
import csv
import os
import re
from datetime import datetime

import cv2

NOMBRE_MODELO = "face_detection_yunet_2023mar.onnx"
URL_MODELO = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/"
    "face_detection_yunet/face_detection_yunet_2023mar.onnx"
)


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
    parser = argparse.ArgumentParser(description="Practica 7 - Deteccion de rostros (OpenCV DNN / YuNet)")
    parser.add_argument(
        "--source", default=None,
        help="Ruta a una foto/video, indice de camara local (ej. 0), o URL de "
             "IP Webcam. Si se omite, se muestra un menu interactivo.",
    )
    parser.add_argument("--score-min", type=float, default=0.7, help="Confianza minima (0-1) para aceptar una deteccion")
    parser.add_argument("--mirror", action="store_true", help="Aplica efecto espejo (webcam frontal)")
    return parser.parse_args()


def crear_carpetas(base_dir):
    capturas_dir = os.path.join(base_dir, "capturas")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(capturas_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    return capturas_dir, logs_dir


def crear_detector(base_dir, score_min):
    modelo = os.path.join(base_dir, "modelos", NOMBRE_MODELO)
    if not os.path.isfile(modelo):
        raise FileNotFoundError(
            f"No se encontro el modelo de deteccion facial en: {modelo}\n"
            f"Descargalo (una sola vez) desde:\n  {URL_MODELO}\n"
            f"y colocalo en la carpeta 'modelos/' de esta practica."
        )
    return cv2.FaceDetectorYN_create(modelo, "", (320, 320), score_threshold=score_min)


def detectar_rostros(detector, frame):
    h, w = frame.shape[:2]
    detector.setInputSize((w, h))
    ok, deteccion = detector.detect(frame)
    resultados = []
    if deteccion is not None:
        for fila in deteccion:
            x, y, w_, h_ = fila[0], fila[1], fila[2], fila[3]
            score = fila[-1]
            resultados.append({
                "x": max(0, int(x)), "y": max(0, int(y)),
                "w": int(w_), "h": int(h_), "score": float(score),
            })
    return resultados


def dibujar_rostros(frame, rostros):
    for i, r in enumerate(rostros, start=1):
        x, y, w, h, score = r["x"], r["y"], r["w"], r["h"], r["score"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame, f"Rostro {i} ({score * 100:.0f}%)", (x, max(y - 10, 15)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2,
        )
    return frame


def elegir_fuente(args):
    if args.source:
        return resolve_source(args.source)

    print("Selecciona la fuente:")
    print("  1) Ruta a una fotografia propia (archivo)")
    print("  2) Webcam local (indice 0)")
    print("  3) IP Webcam (ingresar URL)")
    opcion = input("Opcion [1/2/3] (default 2): ").strip() or "2"

    if opcion == "1":
        ruta = input("Ruta de la fotografia: ").strip()
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"No se encontro la imagen: {ruta}")
        return ruta
    if opcion == "3":
        url = input("URL de IP Webcam (ej. http://192.168.100.146:8080): ").strip()
        return resolve_source(url)
    return 0


def modo_imagenes(rutas, detector, capturas_dir, log_writer, log_file):
    indice = 0
    contador_capturas = 0
    print("Controles: [s] guardar captura   [n] siguiente imagen   [q] salir")
    while True:
        ruta = rutas[indice]
        original = cv2.imread(ruta)
        if original is None:
            raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")

        frame = original.copy()
        rostros = detectar_rostros(detector, frame)
        dibujar_rostros(frame, rostros)
        cv2.putText(frame, os.path.basename(ruta), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        if not rostros:
            cv2.putText(frame, "Sin rostros detectados", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

        cv2.imshow("Practica 7 - Deteccion de rostros", frame)
        key = cv2.waitKey(30) & 0xFF
        if key in (ord("q"), 27):
            break
        elif key == ord("n"):
            indice = (indice + 1) % len(rutas)
        elif key == ord("s"):
            contador_capturas += 1
            nombre_archivo = f"{os.path.splitext(os.path.basename(ruta))[0]}_{contador_capturas}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(os.path.join(capturas_dir, nombre_archivo), frame)
            for i, r in enumerate(rostros, start=1):
                log_writer.writerow([
                    datetime.now().isoformat(timespec="seconds"), os.path.basename(ruta),
                    i, f"{r['score']:.3f}", r["x"], r["y"], r["w"], r["h"],
                ])
            log_file.flush()
            print(f"Captura guardada: {nombre_archivo} ({len(rostros)} rostro(s) detectado(s))")


def modo_video(fuente, args, detector, capturas_dir, log_writer, log_file):
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

            rostros = detectar_rostros(detector, frame)
            dibujar_rostros(frame, rostros)
            cv2.imshow("Practica 7 - Deteccion de rostros", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("s"):
                contador_capturas += 1
                nombre_archivo = f"webcam_{contador_capturas}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                cv2.imwrite(os.path.join(capturas_dir, nombre_archivo), frame)
                for i, r in enumerate(rostros, start=1):
                    log_writer.writerow([
                        datetime.now().isoformat(timespec="seconds"), "webcam",
                        i, f"{r['score']:.3f}", r["x"], r["y"], r["w"], r["h"],
                    ])
                log_file.flush()
                print(f"Captura guardada: {nombre_archivo} ({len(rostros)} rostro(s) detectado(s))")
    finally:
        cap.release()


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    capturas_dir, logs_dir = crear_carpetas(base_dir)
    detector = crear_detector(base_dir, args.score_min)

    log_path = os.path.join(logs_dir, "rostros.csv")
    log_is_new = not os.path.exists(log_path)
    log_file = open(log_path, "a", newline="", encoding="utf-8")
    log_writer = csv.writer(log_file)
    if log_is_new:
        log_writer.writerow(["timestamp", "fuente", "rostro_num", "score", "x", "y", "w", "h"])

    fuente = elegir_fuente(args)

    try:
        if isinstance(fuente, str) and fuente.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            modo_imagenes([fuente], detector, capturas_dir, log_writer, log_file)
        else:
            modo_video(fuente, args, detector, capturas_dir, log_writer, log_file)
    finally:
        cv2.destroyAllWindows()
        log_file.close()


if __name__ == "__main__":
    main()
