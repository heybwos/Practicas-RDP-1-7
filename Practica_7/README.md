# Práctica 7 — Detección de rostros (versión Python)

Equivalente en Python de la aplicación original AFORGE Movimiento Rostro (Visual
Basic). Detecta rostros en una fotografía o en video de cámara en tiempo real —
en vez de solo ejecutar un `.exe` y tomar capturas.

## Nota técnica importante: por qué DNN (YuNet) y no Haar Cascades

Los tutoriales clásicos de OpenCV para detección de rostros usan
`cv2.CascadeClassifier` con un archivo `haarcascade_frontalface_default.xml`. En
la versión de `opencv-python` instalada en este equipo (**OpenCV 5.0**),
`cv2.CascadeClassifier` **ya no existe** (el proyecto OpenCV lo retiró en favor de
detectores basados en redes neuronales). El reemplazo oficial es
**YuNet** (`cv2.FaceDetectorYN`), un modelo ligero en formato ONNX, más preciso
que Haar Cascades y mantenido por el propio equipo de OpenCV en su
["Model Zoo"](https://github.com/opencv/opencv_zoo).

El modelo (`modelos/face_detection_yunet_2023mar.onnx`, ~230 KB) ya está incluido
en esta carpeta, así que no hace falta descargar nada para usar el script. Si en
algún momento falta el archivo, se puede volver a descargar desde:
```
https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
```
y colocarlo en `modelos/`.

## Cómo funciona

1. **Detección:** `cv2.FaceDetectorYN_create(...)` carga el modelo YuNet;
   `detector.detect(frame)` devuelve, por cada rostro encontrado, su bounding box
   y una confianza (`score`, 0–1). Solo se aceptan detecciones con confianza igual
   o mayor a `--score-min` (default 0.7).
2. **Overlay:** se dibuja un rectángulo verde por rostro con su número y
   confianza (ej. `Rostro 1 (94%)`).
3. **Registro:** al guardar (`s`) se anexa a `logs/rostros.csv` una fila por cada
   rostro detectado (timestamp, fuente, número de rostro, score, x, y, w, h).

## Requisitos

```
pip install -r requirements.txt
```

## Imágenes de prueba

A diferencia de las prácticas 2, 4 y 6, aquí **no se incluyen fotografías de
prueba**: un detector de rostros necesita una foto real de una persona para dar
resultados significativos (una imagen sintética/dibujada no sirve como prueba
confiable). Usa tu propia foto (opción 1 del menú) o la cámara en vivo.

## Uso

### Menú interactivo (recomendado)
```
python deteccion_rostro.py
```
```
Selecciona la fuente:
  1) Ruta a una fotografia propia (archivo)
  2) Webcam local (indice 0)
  3) IP Webcam (ingresar URL)
Opcion [1/2/3] (default 2):
```

### Con celular + app "IP Webcam" (Android)
```
python deteccion_rostro.py --source http://192.168.1.XX:8080
```

### Controles

| Acción | Efecto |
|---|---|
| `s` | Guarda una captura de pantalla en `capturas/` y registra los rostros detectados en `logs/rostros.csv` |
| `n` | Siguiente imagen (solo en modo imagen, si cargas varias con `--source`) |
| `q` / `ESC` | Sale del programa |

Repite esto con las 4 imágenes que pide la práctica original (2 fotografías +
2 capturas de webcam), y prueba distintos ángulos/expresiones frente a la cámara
para validar la robustez del detector, como pide la práctica.

Parámetro opcional para ajustar sensibilidad (confianza mínima 0.0–1.0):
```
python deteccion_rostro.py --source 0 --score-min 0.6 --mirror
```

## Archivos generados (no versionados de antemano)

- `capturas/` — screenshots con los rostros etiquetados (número + confianza)
- `logs/rostros.csv` — histórico de todos los rostros detectados y guardados

## Relación con los requisitos del reporte original

- **Marco teórico:** puede basarse en detección de rostros con redes neuronales
  ligeras (YuNet), explicando por qué reemplazó a Haar Cascades en OpenCV 5, en
  vez del texto genérico de Arduino/IR que trae la plantilla original del Notion
  (ver `contexto.md` en la raíz del repositorio).
- **Desarrollo / evidencia fotográfica:** capturas etiquetadas con confianza por
  rostro + `logs/rostros.csv` como tabla de resultados numéricos, útil para
  "validar la respuesta del sistema ante distintos ángulos y expresiones" como
  pide la práctica.
