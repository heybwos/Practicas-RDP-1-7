# Práctica 6 — Lector de códigos de barras (versión Python)

Equivalente en Python de la aplicación original AFORGE Lector Bar Code (Visual
Basic). Lee y decodifica códigos de barras en una imagen o en video de cámara en
tiempo real usando **pyzbar** (bindings de la librería ZBar) — en vez de solo
ejecutar un `.exe` y tomar capturas.

## Cómo funciona

1. **Decodificación:** `pyzbar.decode(frame)` analiza la imagen/frame y devuelve,
   por cada código de barras que encuentra: el tipo (`CODE128`, `EAN13`, `QRCODE`,
   etc.), el dato decodificado (la secuencia numérica/alfanumérica original) y su
   posición (bounding box).
2. **Overlay:** se dibuja un rectángulo verde sobre el código y una etiqueta con
   `tipo: dato_decodificado`.
3. **Registro:** al guardar (`s`) se anexa a `logs/codigos.csv` una fila por cada
   código detectado (timestamp, fuente, tipo, dato decodificado).

## Requisitos

```
pip install -r requirements.txt
```
**Nota (Windows):** `pyzbar` en Windows requiere la DLL de ZBar — el wheel oficial
de `pyzbar` para Windows ya la incluye, así que con `pip install pyzbar` basta (no
hace falta instalar ZBar por separado). En Linux se necesita además el paquete de
sistema `libzbar0` (`sudo apt install libzbar0`).

## Códigos de barras de prueba

El repo incluye `imagenes/codigo_1.png` (Code128 con el valor `123456789012`) e
`imagenes/codigo_2.png` (Code128 con el valor `RECPATRONES2026`), generados
localmente con la librería `python-barcode` (sin depender de internet ni de tener
códigos impresos a la mano). Para regenerarlos o cambiar el valor codificado:
```
python generar_codigos_prueba.py
```

## Uso

### Menú interactivo (recomendado)
```
python lector_barcode.py
```
```
Selecciona la fuente:
  1) Codigos de barras de prueba incluidos
  2) Ruta a una imagen propia
  3) Webcam local (indice 0)
  4) IP Webcam (ingresar URL)
Opcion [1/2/3/4] (default 1):
```

- **Opciones 1 y 2 (imagen estática):** decodifica una vez y muestra el
  resultado; `n` pasa al siguiente código si hay varios cargados.
- **Opciones 3 y 4 (video en vivo):** lectura continua en tiempo real — útil para
  leer códigos de barras reales (de productos, por ejemplo) con la cámara.

### Con celular + app "IP Webcam" (Android)
```
python lector_barcode.py --source http://192.168.1.XX:8080
```

### Controles

| Acción | Efecto |
|---|---|
| `s` | Guarda una captura de pantalla en `capturas/` y registra los códigos leídos en `logs/codigos.csv` |
| `n` | Siguiente imagen de prueba (solo en modo imágenes) |
| `q` / `ESC` | Sale del programa |

Repite esto con al menos 4 códigos de barras distintos (los 2 incluidos + 2
propios, o fotografiando códigos reales con la cámara), tomando 3 capturas de la
codificación numérica de cada uno, como pide la práctica original.

## Archivos generados (no versionados de antemano)

- `capturas/` — screenshots con el código y su valor decodificado etiquetados
- `logs/codigos.csv` — histórico de todos los códigos leídos y guardados

## Relación con los requisitos del reporte original

- **Marco teórico:** puede basarse en cómo codifica Code128 (ancho de barras =
  símbolos) y cómo ZBar/pyzbar los decodifica, en vez del texto genérico de
  Arduino/IR que trae la plantilla original del Notion (ver `contexto.md` en la
  raíz del repositorio).
- **Desarrollo / evidencia fotográfica:** capturas etiquetadas con el valor
  decodificado + `logs/codigos.csv` como tabla de resultados numéricos, ideal
  para comprobar "confiabilidad del sistema" (lecturas repetidas vs. dato original).
