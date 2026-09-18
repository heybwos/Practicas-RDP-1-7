# Práctica 1 — Detección y seguimiento por color (versión Python)

Equivalente en Python de la aplicación original AFORGE Color: Detección y
Seguimiento (Visual Basic). Aquí el algoritmo real de segmentación por color y
seguimiento de centroide está implementado con OpenCV, en vez de solo ejecutar
un `.exe` y tomar capturas.

## Cómo funciona

1. **Selección del color de referencia:** haces clic sobre el objeto que quieres
   seguir en la ventana de video. El script muestrea una pequeña región (16×16 px)
   alrededor del clic en espacio de color **HSV** y calcula su color promedio.
2. **Segmentación por color:** en cada frame siguiente, se genera una máscara
   binaria con `cv2.inRange`, marcando los píxeles cuyo HSV cae dentro de una
   tolerancia (`--tol-h/-s/-v`) alrededor del color de referencia.
3. **Limpieza morfológica:** apertura + dilatación para quitar ruido de la máscara.
4. **Contorno, bounding box y centroide:** igual que en la Práctica 3, se toma el
   contorno más grande por encima de `--min-area` y se calcula su centroide con
   momentos de imagen.
5. **Seguimiento (estela) y registro:** el centroide se dibuja como una estela y
   se anexa a `logs/trayectoria.csv` (timestamp, nombre del objeto, frame, X, Y,
   área), listo para graficar con `graficar_trayectorias.py`.

> Nota técnica: el matiz (H) en OpenCV es circular (0–179) y este script no
> maneja el "wrap-around" cerca de 0/179 (tonos rojos muy saturados). Si el color
> elegido está cerca de ese límite, sube `--tol-h` o elige un objeto de otro color
> para la demo.

## Requisitos

```
pip install -r requirements.txt
```

## Uso

### Menú interactivo (recomendado)
```
python deteccion_color.py
```
Si no le pasas `--source`, el script pregunta qué fuente usar:

```
Selecciona la fuente de video:
  1) Video de prueba: circulos de colores (varios objetos, colores distintos) (circulos_colores.mp4)
  2) Video de prueba: dots (punto rojo en movimiento) (dots.mp4)
  3) Video de prueba: mosca (insecto oscuro en movimiento) (mosca.mp4)
  4) Webcam local (indice 0)
  5) IP Webcam (ingresar URL)
Opcion [1-5] (default 1):
```

- **`videos/circulos_colores.mp4` (recomendado para esta práctica):** varios
  círculos de colores distintos (azul, amarillo, rojo, verde) moviéndose a la vez
  por la pantalla. Es el mejor ejemplo para demostrar segmentación por color de
  verdad: al hacer clic sobre uno de los círculos, el algoritmo lo sigue e
  **ignora correctamente los demás** aunque estén en pantalla al mismo tiempo
  (verificado: con cualquier color elegido, nunca detecta más de un contorno
  grande simultáneo). Prueba clicando distintos círculos para ver cómo cambia
  el objeto seguido.
- **`videos/dots.mp4`:** un punto que se mueve por la pantalla, junto a varias
  cruces estáticas de referencia. El punto **cambia de color con el tiempo**
  (alterna entre negro y rojo saturado en distintos tramos del video) — haz clic
  sobre él mientras esté en la fase roja para ver el ejemplo "de libro" de
  segmentación por color; si haces clic durante la fase negra, el algoritmo lo
  sigue igual (por brillo bajo) pero lo pierde en cuanto cambia a rojo, ya que el
  color de referencia ya no coincide — buen ejemplo real de la limitación de
  trackear un solo color fijo, útil para el marco teórico del reporte.
- **`videos/mosca.mp4`:** funciona bien para la demo aunque las moscas son
  oscuras sobre fondo claro — el color de referencia termina siendo un tono de
  brillo (V) bajo, así que el algoritmo las segmenta por "objeto oscuro sobre
  fondo claro", un caso válido de segmentación por color/intensidad.
- Para un ejemplo más vistoso con color realmente saturado, usa un objeto de
  color (pelota, tapa, etc.) frente a la webcam.
- **Webcam local:** `python deteccion_color.py --source 0`
- **IP Webcam (celular):** ver sección abajo.

### Con celular + app "IP Webcam" (Android)
1. Abre la app **IP Webcam**, presiona "Iniciar servidor" y anota la URL (algo
   como `http://192.168.1.XX:8080`). Celular y PC deben estar en la misma red WiFi.
2. Ejecuta:
   ```
   python deteccion_color.py --source http://192.168.1.XX:8080
   ```
3. Como normalmente se usa la cámara trasera del celular, **no** actives el efecto
   espejo (default). Si usas la cámara frontal, agrega `--mirror`.

### Controles durante la ejecución

| Acción | Efecto |
|---|---|
| Clic izquierdo sobre el video | Toma el color del punto clicado como referencia a seguir |
| `s` | Guarda una captura de pantalla en `capturas/` |
| `n` | Cambia de objeto: pide nuevo nombre y espera un nuevo clic para recalibrar el color |
| `q` / `ESC` | Sale del programa |

Repite esto con los 2 objetos que pide la práctica original (colores distintos),
y guarda al menos una captura por objeto con `s`.

Parámetros opcionales:
```
python deteccion_color.py --source 0 --min-area 500 --tol-h 12 --tol-s 60 --tol-v 60 --mirror
```

## Graficar las trayectorias para el reporte

Con datos ya guardados en `logs/trayectoria.csv`:
```
python graficar_trayectorias.py
```
Genera `capturas/trayectorias.png` con una línea de color por objeto seguido.

## Archivos generados (no versionados de antemano)

- `capturas/` — screenshots (`s`) + `trayectorias.png`
- `logs/trayectoria.csv` — histórico de todas las corridas (se va anexando)

## Relación con los requisitos del reporte original

- **Contenido de la práctica:** los 2 objetos probados + capturas quedan
  cubiertos con la tecla `s` durante la prueba.
- **Marco teórico:** puede basarse en segmentación por color en espacio HSV,
  `cv2.inRange`, morfología y momentos de imagen usados aquí (a diferencia del
  texto genérico de Arduino/IR que trae la plantilla original del Notion — ver
  `contexto.md` en la raíz del repositorio).
- **Desarrollo / evidencia fotográfica:** capturas individuales por objeto +
  `trayectorias.png` con el resumen de los recorridos.
