# Práctica 3 — Detección de movimiento (versión Python)

Equivalente en Python de la aplicación original en AForge.NET/Visual Basic. En vez
de solo ejecutar un `.exe` y tomar capturas, aquí se implementa el algoritmo real de
detección de movimiento y seguimiento de centroide con OpenCV, para que el reporte
pueda explicar el proceso técnico (marco teórico) con base en código propio.

## Cómo funciona

1. **Sustracción de fondo (MOG2):** cada frame de la webcam se compara contra un
   modelo de fondo que se va actualizando (`cv2.createBackgroundSubtractorMOG2`).
   Los píxeles que cambian respecto al fondo quedan marcados en una máscara binaria.
2. **Limpieza morfológica:** se eliminan sombras y ruido de la máscara (apertura +
   dilatación) para quedarnos solo con regiones de movimiento reales.
3. **Contornos y centroide:** se toma el contorno más grande por encima de un área
   mínima (`--min-area`) como "el objeto en movimiento", y se calcula su centroide
   con momentos de imagen (`cv2.moments`).
4. **Seguimiento (estela):** el centroide de cada frame se guarda en una cola de
   longitud fija y se dibuja como una línea de recorrido sobre el video en vivo. Si
   el objeto se pierde por varios frames, la estela se corta (para no unir
   movimientos que no están relacionados).
5. **Registro:** cada posición detectada se anexa a `logs/trayectoria.csv`
   (timestamp, nombre del objeto, frame, X, Y, área).

## Requisitos

```
pip install -r requirements.txt
```
(`opencv-python` y `matplotlib` ya están instalados en este equipo.)

## Uso

### Menú interactivo (recomendado)
```
python deteccion_movimiento.py
```
Si no le pasas `--source`, el script pregunta qué fuente usar:

```
Selecciona la fuente de video:
  1) Video de prueba (mosca.mp4)
  2) Webcam local (indice 0)
  3) IP Webcam (ingresar URL)
Opcion [1/2/3] (default 1):
```

### Video de prueba (`videos/mosca.mp4`)
Ya incluido en el repo: un video corto de moscas moviéndose, útil para probar el
algoritmo sin necesidad de cámara. El video hace *loop* automático al llegar al
final y se reproduce respetando su framerate original (30 FPS). Se puede forzar
directamente sin pasar por el menú:
```
python deteccion_movimiento.py --source videos/mosca.mp4
```
Para usar otro video de prueba, reemplaza el archivo o apunta a otra ruta con
`--source <ruta al video>`.

### Con celular + app "IP Webcam" (Android)
1. Abre la app **IP Webcam**, presiona "Iniciar servidor" y anota la URL que
   muestra (algo como `http://192.168.1.XX:8080`). El celular y la PC deben estar
   en la **misma red WiFi**.
2. Ejecuta:
   ```
   python deteccion_movimiento.py --source http://192.168.1.XX:8080
   ```
   (Si solo das `host:puerto` sin ruta, el script agrega automáticamente `/video`,
   que es el endpoint del stream MJPEG de la app.)
3. Como normalmente se usa la cámara trasera del celular, **no** actives el efecto
   espejo (déjalo desactivado, es el default). Si en algún caso usas la cámara
   frontal del celular y se ve al revés, agrega `--mirror`.

Al iniciar pide el nombre del objeto que vas a probar (ej. `pelota_roja`). Controles
durante la ejecución:

| Tecla | Acción |
|---|---|
| `s` | Guarda una captura de pantalla en `capturas/` con el bounding box y la estela dibujados |
| `n` | Cambia el nombre del objeto actual (limpia la estela para no mezclar recorridos) |
| `q` / `ESC` | Sale del programa |

Repite esto con los 3 objetos que pide la práctica original, moviéndolos de forma
distinta cada vez, y guarda al menos una captura por objeto con `s`.

Parámetros opcionales:

```
python deteccion_movimiento.py --source 0 --min-area 800 --trail-len 64 --lost-frames 15 --mirror
```

## Graficar las trayectorias para el reporte

Una vez que ya probaste los 3 objetos y tienes datos en `logs/trayectoria.csv`:

```
python graficar_trayectorias.py
```

Genera `capturas/trayectorias.png` con una línea por objeto (color propio, inicio =
círculo, fin = cuadrado), lista para insertarse en la sección de "Desarrollo /
Resultados numéricos" del reporte.

## Archivos generados (no versionados de antemano)

- `capturas/` — screenshots (`s`) + `trayectorias.png`
- `logs/trayectoria.csv` — histórico de todas las corridas (se va anexando)

## Relación con los requisitos del reporte original

- **Contenido de la práctica:** los 3 objetos probados + 3 capturas ya quedan
  cubiertos con la tecla `s` durante la prueba.
- **Marco teórico:** puede basarse en la sustracción de fondo MOG2, morfología y
  momentos de imagen usados aquí (a diferencia del texto genérico de Arduino/IR que
  trae la plantilla original del Notion — ver `contexto.md` en la raíz del
  repositorio para más detalle).
- **Desarrollo / evidencia fotográfica:** capturas individuales por objeto +
  `trayectorias.png` con el resumen de los 3 recorridos.
