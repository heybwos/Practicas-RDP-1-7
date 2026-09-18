# Práctica 4 — Detección de formas geométricas (versión Python)

Equivalente en Python de la aplicación original AFORGE Formas Webcam (Visual
Basic). Detecta figuras básicas (triángulo, cuadrado, rectángulo, pentágono,
hexágono, círculo) en imágenes o en video de cámara en tiempo real, usando
contornos y aproximación poligonal con OpenCV — en vez de solo ejecutar un `.exe`
y tomar capturas.

## Cómo funciona

1. **Preprocesado:** escala de grises + `cv2.GaussianBlur` para reducir ruido.
2. **Bordes adaptativos:** se calcula un umbral con Otsu (`cv2.threshold` +
   `THRESH_OTSU`) y se usa para fijar los umbrales de `cv2.Canny` automáticamente
   según el contraste de cada imagen.
3. **Contornos y aproximación poligonal:** `cv2.findContours` + `cv2.approxPolyDP`
   reducen cada contorno a su polígono más simple.
4. **Clasificación por número de vértices:**
   - 3 vértices → Triángulo
   - 4 vértices → Cuadrado (si ancho≈alto) o Rectángulo
   - 5 vértices → Pentágono, 6 → Hexágono
   - Más de 6 vértices → se mide la **circularidad** (`4π·área/perímetro²`); si es
     alta (>0.75) se clasifica como Círculo.
5. **Registro:** cada figura detectada al guardar (`s`) se anexa a
   `logs/formas.csv` (timestamp, fuente, forma, vértices, área, centroide).

## Requisitos

```
pip install -r requirements.txt
```

## Imágenes de prueba

El repo incluye `imagenes/formas_1.png` y `imagenes/formas_2.png` (generadas
sintéticamente, sin depender de internet) con triángulo, cuadrado, rectángulo,
círculo, pentágono y hexágono. Para regenerarlas:
```
python generar_imagenes_prueba.py
```

## Uso

### Menú interactivo (recomendado)
```
python deteccion_formas.py
```
```
Selecciona la fuente:
  1) Imagenes de prueba incluidas (formas geometricas)
  2) Ruta a una imagen propia
  3) Webcam local (indice 0)
  4) IP Webcam (ingresar URL)
Opcion [1/2/3/4] (default 1):
```

- **Opciones 1 y 2 (imagen estática):** se detectan las formas una vez y se
  muestran superpuestas; `n` pasa a la siguiente imagen (si hay varias).
- **Opciones 3 y 4 (video en vivo):** detección continua en tiempo real, útil
  para las 2 capturas de webcam que pide la práctica.

### Con celular + app "IP Webcam" (Android)
Igual que en las prácticas anteriores: abre la app, presiona "Iniciar servidor",
anota la URL (`http://192.168.1.XX:8080`) y úsala en la opción 4 del menú, o
directamente:
```
python deteccion_formas.py --source http://192.168.1.XX:8080
```

### Controles

| Acción | Efecto |
|---|---|
| `s` | Guarda una captura de pantalla en `capturas/` y registra las figuras detectadas en `logs/formas.csv` |
| `n` | Siguiente imagen de prueba (solo en modo imágenes) |
| `q` / `ESC` | Sale del programa |

Sigue el requisito original: 3 capturas de formas observadas en 4 imágenes
distintas (2 imágenes de prueba/propias + 2 capturas de webcam).

Parámetro opcional para ajustar sensibilidad:
```
python deteccion_formas.py --source 0 --min-area 800 --mirror
```

## Archivos generados (no versionados de antemano)

- `capturas/` — screenshots con las formas etiquetadas
- `logs/formas.csv` — histórico de todas las figuras detectadas y guardadas

## Relación con los requisitos del reporte original

- **Marco teórico:** puede basarse en detección de bordes (Canny), contornos,
  aproximación poligonal (`approxPolyDP`) y circularidad usados aquí (a
  diferencia del texto genérico de Arduino/IR que trae la plantilla original del
  Notion — ver `contexto.md` en la raíz del repositorio).
- **Desarrollo / evidencia fotográfica:** capturas etiquetadas + `logs/formas.csv`
  como tabla de resultados numéricos (forma, vértices, área, posición).
