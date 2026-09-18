# Práctica 2 — Parámetros de imagen: brillo, contraste y saturación (versión Python)

Equivalente en Python de la aplicación original AFORGE Parámetro Imagen (Visual
Basic). En vez de solo ejecutar un `.exe` y tomar capturas, aquí se implementa el
ajuste real de brillo/contraste/saturación con OpenCV y barras deslizantes en vivo.

## Cómo funciona

1. **Brillo y contraste:** `cv2.convertScaleAbs(img, alpha=contraste, beta=brillo)`
   — `alpha` escala la intensidad de los píxeles (contraste) y `beta` suma un
   offset constante (brillo).
2. **Saturación:** la imagen se convierte a **HSV**, se escala el canal S
   (saturación) por un factor y se recorta a `[0, 255]`, y se vuelve a convertir
   a BGR.
3. **Vista en vivo:** tres barras deslizantes (`Brillo`, `Contraste x100`,
   `Saturacion x100`) controlan los tres parámetros; la ventana muestra la imagen
   **original** y la **modificada** lado a lado, actualizándose en tiempo real.
4. **Registro:** al guardar (`s`) se escriben ambas imágenes en `capturas/` y se
   anexa una fila a `logs/parametros.csv` con los valores exactos usados
   (brillo, contraste, saturación) — útil como "resultados numéricos" en el reporte.

## Requisitos

```
pip install -r requirements.txt
```

## Imágenes de prueba

El repo ya incluye dos imágenes sintéticas generadas sin depender de internet
(`imagenes/prueba_1.png` y `imagenes/prueba_2.png`) para poder probar el script
sin necesidad de cámara. Si quieres regenerarlas (o modificar los patrones):
```
python generar_imagenes_prueba.py
```

## Uso

### Menú interactivo (recomendado)
```
python parametros_imagen.py
```
Te pregunta el origen de la imagen:
```
Selecciona el origen de la(s) imagen(es):
  1) Imagenes de prueba incluidas
  2) Ruta a un archivo de imagen propio
  3) Capturar una foto con camara (webcam o IP Webcam)
Opcion [1/2/3] (default 1):
```
- **Opción 1:** carga `imagenes/prueba_1.png` y `imagenes/prueba_2.png`; usa `n`
  para alternar entre ellas.
- **Opción 2:** pide la ruta de una imagen tuya (jpg/png/etc).
- **Opción 3:** abre la webcam local o una IP Webcam (te pide la fuente), y con
  `ESPACIO` tomas la foto que se va a usar (con `ESC` cancelas).

También puedes saltarte el menú indicando la imagen directamente (se puede repetir
`--imagen` para cargar varias):
```
python parametros_imagen.py --imagen imagenes/prueba_1.png --imagen imagenes/prueba_2.png
```

### Controles durante la ejecución

| Acción | Efecto |
|---|---|
| Barra "Brillo" | Ajusta el brillo entre -100 y +100 |
| Barra "Contraste x100" | Ajusta el contraste entre 0.00x y 3.00x |
| Barra "Saturacion x100" | Ajusta la saturación entre 0.00x y 3.00x |
| `s` | Guarda original + modificada en `capturas/` y registra los parámetros en `logs/parametros.csv` |
| `n` | Pasa a la siguiente imagen cargada |
| `q` / `ESC` | Sale del programa |

Repite esto con las 2 imágenes que pide la práctica original, ajustando al menos
dos parámetros distintos por imagen, y guarda con `s` antes/después de cada ajuste.

## Archivos generados (no versionados de antemano)

- `capturas/` — pares `*_original_*.png` / `*_modificada_*.png`
- `logs/parametros.csv` — histórico de todos los ajustes guardados

## Relación con los requisitos del reporte original

- **Contenido de la práctica:** las 2 imágenes + las modificaciones de parámetros
  quedan cubiertas con la tecla `s` (guarda antes/después automáticamente).
- **Marco teórico:** puede basarse en el modelo de color HSV, la transformación
  lineal de brillo/contraste (`alpha`/`beta`) y el escalado del canal de
  saturación usados aquí (a diferencia del texto genérico de Arduino/IR que trae
  la plantilla original del Notion — ver `contexto.md` en la raíz del repositorio).
- **Desarrollo / evidencia fotográfica:** pares original/modificada por imagen +
  `logs/parametros.csv` como tabla de resultados numéricos.
