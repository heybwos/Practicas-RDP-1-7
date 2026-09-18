# Práctica 5 — Fotomatón (versión Python)

Equivalente en Python de la aplicación original AFORGE Fotomatón / "Mis Fotitos"
(Visual Basic). Toma fotos en secuencia desde la cámara y les aplica un filtro de
color y un fondo/marco decorativo, como una cabina fotográfica real — en vez de
solo ejecutar un `.exe` y tomar capturas.

## Cómo funciona

1. **Vista previa en vivo:** la cámara se muestra en tiempo real con el filtro
   actual ya aplicado, para ver el resultado antes de "disparar".
2. **Filtros de color** (tecla `f` para rotar entre ellos):
   - `original`, `grises`, `sepia` (matriz de transformación clásica),
     `invertido`, `frio` (más azul, menos rojo), `calido` (más rojo, menos azul).
3. **Fondo/marco** (tecla `b` para rotar): la foto final se compone sobre un
   lienzo de color con un margen tipo marco de fotomatón (`blanco`, `negro`,
   `rosa_pastel`, `azul_pastel`).
4. **Captura:** `ESPACIO` aplica el filtro y fondo actuales a la foto y la guarda
   en `capturas/`, con un pequeño "flash" visual de confirmación.
5. **Registro:** cada foto guardada se anexa a `logs/fotomaton.csv` (timestamp,
   filtro usado, fondo usado, archivo).

## Requisitos

```
pip install -r requirements.txt
```

## Uso

```
python fotomaton.py
```
Si no le pasas `--source`, pregunta qué cámara usar:
```
Selecciona la camara:
  1) Webcam local (indice 0)
  2) IP Webcam (ingresar URL)
Opcion [1/2] (default 1):
```

### Con celular + app "IP Webcam" (Android)
Abre la app, presiona "Iniciar servidor", anota la URL y úsala:
```
python fotomaton.py --source http://192.168.1.XX:8080
```
Con IP Webcam (cámara trasera normalmente) el espejo se desactiva automáticamente;
para forzarlo de cualquier forma usa `--mirror`.

### Controles

| Tecla | Acción |
|---|---|
| `ESPACIO` | Toma la foto (aplica el filtro y fondo actuales y la guarda) |
| `f` | Cambia al siguiente filtro de color |
| `b` | Cambia al siguiente fondo/marco |
| `q` / `ESC` | Sale del programa |

Repite esto con las 3 modificaciones a 3 imágenes que pide la práctica original
(combina filtro + fondo distintos en cada captura).

## Archivos generados (no versionados de antemano)

- `capturas/` — fotos finales (`foto_<n>_<filtro>_<fondo>_<fecha>.png`)
- `logs/fotomaton.csv` — histórico de filtro/fondo usados en cada foto

## Relación con los requisitos del reporte original

- **Contenido de la práctica:** las 3 modificaciones a 3 imágenes quedan
  cubiertas alternando filtro (`f`) y fondo (`b`) entre capturas (`ESPACIO`).
- **Marco teórico:** puede basarse en transformaciones de color por matriz
  (sepia), aritmética de canales BGR (frío/cálido) y composición de imágenes
  (fondo/marco) usadas aquí (a diferencia del texto genérico de Arduino/IR que
  trae la plantilla original del Notion — ver `contexto.md` en la raíz del
  repositorio).
- **Desarrollo / evidencia fotográfica:** fotos finales con filtro+fondo
  aplicados + `logs/fotomaton.csv` como tabla de resultados.
