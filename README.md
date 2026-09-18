# Laboratorio de Reconocimiento de Patrones — Prácticas en Python

Este repositorio contiene la versión en **Python** de las 7 prácticas del
laboratorio de Reconocimiento de Patrones (originalmente hechas con aplicaciones
`.exe` en Visual Basic / AForge.NET). Aquí, en cambio, cada práctica trae su
propio código fuente con el algoritmo real implementado (usando OpenCV y otras
librerías), para poder explicar de verdad cómo funciona en el reporte, en vez de
solo ejecutar un programa ya hecho.

> Para el contexto completo del laboratorio original (qué pide cada práctica,
> cómo se califica, etc.) ver [`contexto.md`](contexto.md) en esta misma carpeta.

## Cómo está organizado

Cada práctica vive en su propia carpeta (`Practica_1` a `Practica_7`) y es
**independiente**: tiene su propio script, su propio `requirements.txt` y su
propio `README.md` con el detalle técnico completo (parámetros opcionales, cómo
funciona el algoritmo por dentro, controles de teclado, etc.). Puedes copiar o
descargar solo la carpeta de la práctica que necesites y funcionará sola.

## Antes de empezar (una sola vez por práctica)

Necesitas **Python 3** instalado. Dentro de la carpeta de la práctica que vayas a
usar, instala sus dependencias:

```
cd Practica_X
pip install -r requirements.txt
```

(Cada práctica solo pide las librerías que realmente usa, así que no hace falta
instalar todo el repo de una vez.)

## Cómo se ejecutan (patrón general)

Todas se corren igual: entras a la carpeta y ejecutas el script principal con
`python`:

```
cd Practica_1
python deteccion_color.py
```

Si el script necesita una cámara o una imagen y no le indicas cuál usar, te
muestra un **menú en la terminal** preguntando la fuente (por ejemplo: "1) video
de prueba, 2) webcam local, 3) celular"). Solo escribes el número y das Enter.

Casi todas comparten estos controles de teclado (excepto la Práctica 5, que se
explica aparte más abajo):

| Tecla | Qué hace |
|---|---|
| `s` | Guarda una captura de pantalla (para el reporte) |
| `n` | Cambia de imagen/objeto (según la práctica) |
| `q` o `ESC` | Cierra el programa |

Cada práctica guarda sus resultados en dos carpetas que se crean solas al
usarla (no vienen en el repositorio, se generan la primera vez que la corres):

- **`capturas/`** — las imágenes que guardas con `s`
- **`logs/`** — un archivo `.csv` con los datos numéricos de cada corrida
  (posiciones, valores usados, etc.), útil como "resultados numéricos" del reporte

## Usar el celular como cámara (opcional, con la app "IP Webcam")

Las prácticas 1, 3, 4, 5, 6 y 7 pueden usar el celular en vez de (o además de) la
webcam de la laptop:

1. Instala la app **IP Webcam** (Android) en tu celular.
2. Ábrela y presiona **"Iniciar servidor"**.
3. Anota la URL que aparece (algo como `http://192.168.1.XX:8080`). El celular y
   la computadora deben estar conectados a la **misma red WiFi**.
4. Escribe esa URL cuando el menú de la práctica te la pida, o pásala directo sin
   pasar por el menú:
   ```
   python <script>.py --source http://192.168.1.XX:8080
   ```

---

## Las 7 prácticas, explicadas en simple

### Práctica 1 — Detección y seguimiento por color
**Qué hace:** haces clic con el mouse sobre un objeto de cierto color (una
pelota, un punto de color, etc.) en la ventana de video, y el programa lo sigue
automáticamente, dibujando un cuadro verde alrededor y una línea con el
recorrido que ha hecho.

**Cómo ejecutarla:**
```
cd Practica_1
python deteccion_color.py
```

**¿Usa cámara?** Es opcional. Puedes usar tu webcam, el celular (IP Webcam), o
probarla sin cámara con los videos de prueba incluidos.

**Material de apoyo incluido:** 3 videos de prueba en `videos/`:
- `circulos_colores.mp4` — varios círculos de colores distintos moviéndose a la
  vez (el mejor para ver que el programa sí distingue el color que elegiste)
- `dots.mp4` — un punto que se mueve y cambia de color con el tiempo
- `mosca.mp4` — moscas moviéndose (sirve para probar con objetos oscuros)

**Extra:** después de probarla, `python graficar_trayectorias.py` genera una
gráfica con el recorrido del objeto seguido, lista para el reporte.

---

### Práctica 2 — Brillo, contraste y saturación
**Qué hace:** muestra una imagen con 3 barras deslizantes (brillo, contraste,
saturación) que puedes mover en vivo; la ventana te enseña la imagen original y
la modificada una al lado de la otra para comparar.

**Cómo ejecutarla:**
```
cd Practica_2
python parametros_imagen.py
```

**¿Usa cámara?** Es opcional. Puedes usar las imágenes de prueba incluidas, una
imagen propia (le das la ruta del archivo), o tomarte una foto con la webcam/celular.

**Material de apoyo incluido:** 2 imágenes de prueba en `imagenes/` (generadas
por el propio proyecto con figuras y colores, no dependen de internet ni de
fotos de terceros).

---

### Práctica 3 — Detección de movimiento
**Qué hace:** compara cada imagen de la cámara contra el "fondo" (lo que no se
mueve) para encontrar qué se está moviendo, y dibuja un cuadro + una línea con
el recorrido sobre el objeto en movimiento.

**Cómo ejecutarla:**
```
cd Practica_3
python deteccion_movimiento.py
```

**¿Usa cámara?** Es opcional. Puedes usar tu webcam, el celular (IP Webcam), o el
video de prueba incluido.

**Material de apoyo incluido:** `videos/mosca.mp4` — un video corto de moscas
moviéndose, para probar sin necesidad de cámara.

**Extra:** igual que la Práctica 1, `python graficar_trayectorias.py` genera la
gráfica del recorrido.

---

### Práctica 4 — Detección de formas
**Qué hace:** busca figuras geométricas (triángulo, cuadrado, rectángulo,
pentágono, hexágono, círculo) en una imagen o en video, y le pone una etiqueta
con el nombre de la figura a cada una.

**Cómo ejecutarla:**
```
cd Practica_4
python deteccion_formas.py
```

**¿Usa cámara?** Es opcional. Funciona con las imágenes de prueba incluidas, una
imagen propia, la webcam, o el celular.

**Material de apoyo incluido:** 2 imágenes de prueba con varias figuras
geométricas ya dibujadas, en `imagenes/`.

---

### Práctica 5 — Fotomatón
**Qué hace:** funciona como una cabina de fotos: ves la cámara en vivo, eliges un
filtro de color (blanco y negro, sepia, invertido, tono frío/cálido) y un
fondo/marco decorativo, y con la tecla `ESPACIO` tomas la foto ya con esos
efectos aplicados.

**Cómo ejecutarla:**
```
cd Practica_5
python fotomaton.py
```

**¿Usa cámara?** **Sí, es obligatoria** (webcam local o celular con IP Webcam) —
esta es la única práctica que no se puede probar sin cámara, porque necesita
fotografiarte a ti.

**Material de apoyo:** ninguno — todo se genera con la cámara en el momento.

**Controles (distintos al resto):** `ESPACIO` toma la foto, `f` cambia de
filtro, `b` cambia de fondo, `q`/`ESC` sale (no usa `s` ni `n`).

---

### Práctica 6 — Lector de códigos de barras
**Qué hace:** lee un código de barras (apuntando la cámara hacia él, o desde una
imagen) y te muestra en pantalla el número o texto que tiene codificado.

**Cómo ejecutarla:**
```
cd Practica_6
python lector_barcode.py
```

**¿Usa cámara?** Es opcional. Funciona con los códigos de prueba incluidos, una
imagen propia, la webcam, o el celular.

**Material de apoyo incluido:** 2 códigos de barras de prueba en `imagenes/`
(generados por el propio proyecto — no necesitas un código impreso a la mano
para probarlo, aunque también puedes escanear uno real con la cámara).

---

### Práctica 7 — Detección de rostros
**Qué hace:** encuentra caras humanas en una foto o en video en vivo, y dibuja un
cuadro verde alrededor de cada rostro detectado junto con el porcentaje de
confianza (ej. "Rostro 1 (94%)").

**Cómo ejecutarla:**
```
cd Practica_7
python deteccion_rostro.py
```

**¿Usa cámara?** Se recomienda usar la webcam o el celular (IP Webcam); también
puedes usar una fotografía propia dándole la ruta del archivo.

**Material de apoyo incluido:** el modelo de inteligencia artificial que detecta
las caras (`modelos/face_detection_yunet_2023mar.onnx`) ya viene incluido en la
carpeta, no hay que descargar nada aparte. **No se incluyen fotos de prueba**
porque un detector de rostros necesita una cara real de una persona para dar
resultados confiables — una imagen inventada/dibujada no serviría como prueba.

---

## Resumen rápido

| # | Práctica | ¿Necesita cámara? | Material incluido |
|---|---|---|---|
| 1 | Color | No (hay videos de prueba) | 3 videos de prueba |
| 2 | Brillo/contraste/saturación | No (hay imágenes de prueba) | 2 imágenes de prueba |
| 3 | Movimiento | No (hay un video de prueba) | 1 video de prueba |
| 4 | Formas | No (hay imágenes de prueba) | 2 imágenes de prueba |
| 5 | Fotomatón | **Sí, obligatorio** | — |
| 6 | Código de barras | No (hay códigos de prueba) | 2 códigos de prueba |
| 7 | Rostros | Recomendado (o foto propia) | Modelo de IA incluido |

## Más información

- Cada carpeta `Practica_X/` tiene su propio `README.md` con el detalle técnico
  completo: cómo funciona el algoritmo por dentro, todos los parámetros
  opcionales (`--source`, `--min-area`, etc.) y la relación con lo que pide el
  reporte de esa práctica.
- [`contexto.md`](contexto.md) explica el contenido original del laboratorio
  (extraído del Notion del profesor) y por qué se hicieron también estas
  versiones en Python.
