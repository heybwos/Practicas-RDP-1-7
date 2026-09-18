# Contexto — Laboratorio de Reconocimiento de Patrones

> Información extraída del Notion oficial del curso (ver enlace en el archivo `Material`):
> https://extreme-coneflower-bab.notion.site/Laboratorio-Reconocimiento-de-Patrones-1ec84fb33043809faf02f6309ec9720e

## Resumen rápido — qué hace cada práctica

- **Práctica 1:** detecta y sigue un objeto en movimiento con la webcam.
- **Práctica 2:** modifica brillo, contraste y color de una imagen.
- **Práctica 3:** detecta movimiento en video (webcam o grabación).
- **Práctica 4:** detecta formas geométricas en imágenes o webcam.
- **Práctica 5:** toma fotos en secuencia y las edita (tipo cabina fotográfica).
- **Práctica 6:** lee y decodifica códigos de barras.
- **Práctica 7:** detecta rostros en fotos o webcam.

## Datos generales

- **Instructor:** M.A. Alfredo Romero Balboa
- **Institución:** Facultad de Ingeniería Mecánica y Eléctrica (FIME)
- **Email:** aromerob@uanl.edu.mx
- **Horario:** atención a estudiantes de 1pm a 5pm; clases de 5pm a 9pm

## Descripción de la unidad de aprendizaje

La materia "Reconocimiento de patrones" está dividida en 3 unidades temáticas:

1. Conceptos base: adquisición de imágenes (inspirada en el proceso de formación de imágenes del ojo humano) y procesamiento digital de imágenes en dominio espacial y frecuencial.
2. Herramientas y métodos matemáticos para detección, extracción y clasificación de características (patrones).
3. Diseño de modelos funcionales / prototipos de reconocimiento de patrones.

**Propósito:** que el estudiante conozca los principios de ingeniería en que se basan los sistemas y dispositivos de identificación personal (biometría), y sea capaz de diseñar sistemas automáticos manipulados con datos biológicos.

**Habilidades que busca desarrollar:** diseño de soluciones biométricas, reconocimiento de huellas dactilares, reconocimiento facial, reconocimiento de iris, sistemas multibiométricos, análisis de vulnerabilidades y seguridad/privacidad de datos biométricos.

### Metodología de trabajo
- Participación activa en clase.
- Consulta y análisis de fuentes científicas (repositorios, artículos, libros).
- Desarrollo de propuestas de diseño y prototipos.
- Reportes técnicos con diagramas, resultados numéricos y conclusiones.
- Comunicación asíncrona por correo institucional, Google Classroom o MS Teams.

### Recursos
- Plataformas: MS Teams, Google Classroom, correo institucional.
- Dispositivos: laptop, celular o tablet con internet.
- Software: herramientas de simulación electrónica y prototipado (en este caso, las aplicaciones AForge.NET en Visual Basic proporcionadas por el instructor).

### Ponderación del reporte de cada práctica
| Sección | % |
|---|---|
| Portada | 5% |
| Índice | 5% |
| Introducción | 5% |
| Marco teórico | 25% |
| Desarrollo (diseño, fabricación, diagramas, hojas de datos, evidencia fotográfica) | 50% |
| Conclusión | 5% |
| Bibliografía | 5% |

### Entregas
- Todo se sube a **MS Teams** en PDF (no `.rar`), y si se pide, un video `.mp4` demostrando el funcionamiento.
- Formato de nombre de archivo varía por práctica: `Actividad # – Nombre de la actividad` o `Iniciales Materia + Inicial Días + Hora - # de lista - E + # de Equipo – Nombre de la práctica`.
- **Entregas atrasadas:** se descuenta un % por cada 24 h de retraso; si hay una causa justificada hay que avisar al instructor **antes** de la fecha límite.
- **Plagio:** se considera deshonestidad académica grave y se reporta a la subdirección académica.

---

## Estructura común a las 7 prácticas

Todas las prácticas del Notion siguen exactamente la misma plantilla:

1. **Competencia específica** — objetivo general de la práctica.
2. **Elementos de competencia** — 3 sub-objetivos puntuales.
3. **Descripción de la práctica** — qué hace la aplicación proporcionada.
4. **Contenido de la práctica** — pasos a seguir (investigar, ejecutar la app, tomar capturas, explicarlas).
5. **Ruta para ejecutar la aplicación** — ruta del `.exe` dentro del ZIP proporcionado por el profesor.
6. **Elementos del reporte (100%)** — portada, índice, introducción, marco teórico, desarrollo, conclusión, bibliografía.
7. **Archivos proporcionados** / **Cuestionario** — quedan vacíos en el Notion (sin contenido cargado).
8. **Entrega de actividad** — subir PDF a MS Teams.
9. **Ejemplo del procedimiento de diseño** (ilustrativo, ver nota al final) con:
   - Fundamento teórico
   - Procedimiento
   - Seguridad en el laboratorio (12 puntos genéricos de seguridad, iguales en las 7 prácticas)
   - Referencias

A continuación el detalle específico de cada una de las 7 prácticas, cada una a trabajarse en su carpeta `Practica_N`.

---

## Práctica N°1 — AFORGE Color: Detección y Seguimiento
**Carpeta:** `Practica_1/`

- **Competencia específica:** aplicar técnicas de visión por computadora usando una interfaz gráfica para detección y seguimiento de objetos en tiempo real vía webcam.
- **Elementos de competencia:**
  - Investigar los fundamentos de sistemas de detección/seguimiento de objetos.
  - Aplicar la interfaz gráfica en Visual Basic para reconocimiento/seguimiento.
  - Interpretar el comportamiento del sistema mediante capturas y análisis funcional.
- **Descripción:** interfaz gráfica (Visual Studio / Visual Basic) que detecta y sigue un objeto por webcam en tiempo real, sin importar su movimiento.
- **Contenido / pasos:**
  1. Investigar sobre sistemas de detección y seguimiento de objetos.
  2. Ejecutar la app y probarla con 2 objetos diferentes.
  3. Tomar 2 capturas de pantalla (una por objeto en movimiento).
  4. Explicar brevemente lo observado en cada imagen, simulando una aplicación real.
- **Ruta del ejecutable:**
  `AFORGE COLOR\AFORGE DETECCION SEGUIMIENTO\bin\Debug\AFORGE DETECCIÓN SEGUIMIENTO.exe`
- **Entrega:** PDF a MS Teams con formato `Actividad # – Nombre de la actividad`.
- **Referencias sugeridas:** documentación oficial de AForge.NET, material del curso.

---

## Práctica N°2 — AFORGE Parámetro Imagen
**Carpeta:** `Practica_2/`

- **Competencia específica:** desarrollar habilidades para modificar parámetros visuales (brillo, contraste, color) en imágenes digitales mediante una interfaz en Visual Basic con AForge.NET.
- **Elementos de competencia:**
  - Comprender fundamentos del procesamiento digital de imágenes.
  - Aplicar herramientas de software para modificar brillo/contraste/color.
  - Documentar visualmente los cambios realizados.
- **Descripción:** interfaz AForge.NET para aplicar y visualizar modificaciones de brillo, contraste y saturación sobre imágenes estáticas.
- **Contenido / pasos:**
  1. Investigar sobre sistemas de modificación de imágenes.
  2. Aplicar la interfaz a 2 imágenes distintas, ajustando parámetros.
  3. Tomar 2 capturas por cada imagen modificada.
  4. Explicar los cambios realizados y su efecto visual.
- **Ruta del ejecutable:**
  `AFORGE PARAMETROS IMAGEN\AFORGE PARAMETROS IMAGEN\bin\Debug\AFORGE PARAMETROS IMAGEN.exe`
- **Entrega:** PDF a MS Teams, formato `Iniciales Materia + Inicial Días + Hora - # de lista - E + # de Equipo – Nombre de la práctica`.
- **Referencias sugeridas:** documentación de AForge.NET, manual de Visual Basic e interfaces gráficas.

---

## Práctica N°3 — Detección de movimiento
**Carpeta:** `Practica_3/`

- **Competencia específica:** aplicar herramientas de visión por computadora para interpretar y evaluar el seguimiento de objetos en tiempo real mediante una interfaz ya desarrollada en Visual Studio.
- **Elementos de competencia:**
  - Operar la interfaz para iniciar/controlar la detección y seguimiento.
  - Verificar la precisión del seguimiento con distintos movimientos/trayectorias.
  - Analizar la eficiencia del sistema y proponer mejoras.
- **Descripción:** misma base que la práctica 1 (Visual Studio/VB) para detectar y seguir un objeto vía webcam en tiempo real.
- **Contenido / pasos:**
  1. Investigar sobre sistemas de detección de movimiento.
  2. Probar la interfaz con 3 objetos distintos, realizando movimientos distintos.
  3. Tomar 3 capturas (una por objeto).
  4. Explicar brevemente cada movimiento observado.
- **Ruta del ejecutable:**
  `DETECCION MOVIMIENTO\DETECCION MOVIMIENTO\bin\Debug\DETECCION MOVIMIENTO.exe`
- **Entrega:** PDF a MS Teams, formato `Iniciales Materia + Inicial Días + Hora - # de lista - E + # de Equipo – Nombre de la práctica`.
- **Referencias sugeridas:** Arduino.cc, libros de control y sensores, guías de sensores IR, tutoriales de YouTube (nota: este bloque de referencias/fundamento teórico de ejemplo en el Notion no corresponde al tema real de la práctica — ver apartado final).

---

## Práctica N°4 — Formas Webcam
**Carpeta:** `Practica_4/`

- **Competencia específica:** integrar el uso de interfaces gráficas en Visual Studio para observar y analizar imágenes en tiempo real, aplicando detección de formas por webcam.
- **Elementos de competencia:**
  - Manipular la interfaz para visualizar correctamente imágenes capturadas en tiempo real.
  - Explorar y contrastar métodos de detección de formas, relacionando teoría y práctica.
  - Evaluar la efectividad del sistema, identificando ventajas y limitaciones.
- **Descripción:** interfaz en Visual Basic que detecta figuras básicas en una imagen o vía webcam en tiempo real.
- **Contenido / pasos:**
  1. Investigar sobre sistemas de detección de formas.
  2. Aplicar la interfaz y tomar 3 capturas de las formas observadas en 4 imágenes distintas (2 imágenes fijas + 2 capturas de webcam).
  3. Explicar brevemente cada captura (imagen, detección de formas, y qué aplicación real se está simulando).
- **Ruta del ejecutable:**
  `FORMAS WEBCAM\FORMAS\bin\Debug\FORMAS.exe`
- **Entrega:** PDF a MS Teams, formato `Actividad # – Nombre de la actividad`.

---

## Práctica N°5 — Fotomaton
**Carpeta:** `Practica_5/`

- **Competencia específica:** emplear la aplicación Fotomaton en Visual Studio para capturar y personalizar fotografías en secuencia, aplicando edición digital básica.
- **Elementos de competencia:**
  - Operar la interfaz para captura de fotografías en secuencia.
  - Aplicar funciones de edición (cambios de color, fondos) por imagen.
  - Analizar la calidad/resultado de las imágenes generadas.
- **Descripción:** interfaz tipo "cabina fotográfica" (Visual Basic) que toma fotos en secuencia y permite modificarlas (color, fondo, etc.) individualmente.
- **Contenido / pasos:**
  1. Investigar sobre fotografía rápida y fotografía secuencial (cabinas fotográficas).
  2. Aplicar la interfaz: 3 modificaciones sobre 3 imágenes distintas; guardar capturas de la imagen original y modificada.
  3. Explicar brevemente cada captura y su modificación.
- **Ruta del ejecutable:**
  `FOTOMATON\MIS FOTITOS\bin\Debug\MIS FOTITOS.exe`
- **Entrega:** PDF a MS Teams, formato `Actividad # – Nombre de la actividad`.

---

## Práctica N°6 — Lector Bar Code
**Carpeta:** `Practica_6/`

- **Competencia específica:** utilizar la aplicación de lectura de códigos de barras en Visual Studio para identificar y traducir información codificada en secuencias numéricas.
- **Elementos de competencia:**
  - Ejecutar la interfaz para reconocer distintos tipos de etiquetas impresas.
  - Interpretar la información numérica obtenida al decodificar el código de barras.
  - Comprobar la confiabilidad del sistema con lecturas repetidas, comparando contra los datos originales.
- **Descripción:** interfaz en Visual Basic que lee códigos de barras y los codifica en una secuencia numérica.
- **Contenido / pasos:**
  1. Investigar sobre sistemas de lectura de códigos de barras.
  2. Aplicar la interfaz: 3 capturas de la codificación numérica de 4 códigos de barras distintos.
  3. Explicar brevemente cada captura y su codificación.
- **Ruta del ejecutable:**
  `LECTOR BARCODE\LECTOR BARCODE\bin\Debug\LECTOR BARCODE.exe`
- **Entrega:** PDF a MS Teams, formato `Actividad # – Nombre de la actividad`.

---

## Práctica N°7 — Movimiento Rostro
**Carpeta:** `Practica_7/`

- **Competencia específica:** aplicar técnicas de reconocimiento facial mediante una interfaz en Visual Studio, identificando rostros en imágenes y video en tiempo real.
- **Elementos de competencia:**
  - Utilizar la aplicación para detectar rostros en fotografías y en secuencias de webcam.
  - Validar la respuesta del sistema ante distintos ángulos y expresiones.
  - Reflexionar sobre aplicaciones prácticas del reconocimiento facial (seguridad, interacción, control).
- **Descripción:** interfaz en Visual Basic que detecta el rostro de una persona en fotografías y/o webcam en tiempo real.
- **Contenido / pasos:**
  1. Investigar sobre sistemas detectores de rostros.
  2. Aplicar la interfaz: 3 capturas sobre 4 imágenes distintas (2 fotografías + 2 fotos de webcam).
  3. Explicar brevemente cada captura y su selección.
- **Ruta del ejecutable:**
  `MOVIMIENTO ROSTRO\MOVIMIENTO ROSTRO\bin\Debug\MOVIMIENTO ROSTRO.exe`
- **Entrega:** PDF a MS Teams, formato `Actividad # – Nombre de la actividad`.

---

## Seguridad en el laboratorio (aplica a las 7 prácticas)

1. Usar calzado cerrado y pantalón completo dentro del laboratorio.
2. Usar equipo de protección personal (bata, gafas, guantes) si se indica.
3. Evitar tocar componentes electrónicos con las manos desnudas; usar protección antiestática y tocar solo el aislante.
4. No trabajar con corriente eléctrica sin supervisión o conocimiento adecuado.
5. No fumar, vapear, comer ni beber en el laboratorio.
6. Mantener el área de trabajo limpia y ordenada.
7. Leer cuidadosamente instrucciones y manuales antes de usar el equipo.
8. Verificar que los circuitos estén bien conectados antes de energizarlos.
9. No trabajar en circuitos energizados.
10. Usar herramientas apropiadas para componentes y cables.
11. Conocer la ubicación de extintores e interruptores de emergencia.
12. Notificar de inmediato cualquier accidente o peligro potencial.

---

## Apartado final: sobre el comentario del ingeniero ("el Notion está muy simple, hazlo también en Python")

Sí, es una observación válida — al extraer y revisar el contenido completo del Notion se confirma:

1. **Las 7 prácticas no piden programar nada.** Todas siguen el mismo molde: el profesor entrega un `.exe` ya compilado (interfaces hechas en **Visual Studio / Visual Basic** con la librería **AForge.NET**), y la actividad del alumno se reduce a: investigar un poco, abrir la app, probarla con webcam o imágenes, tomar capturas de pantalla y redactar un reporte en PDF (portada, marco teórico, desarrollo, conclusión, bibliografía). No hay entregable de código en ninguna de las 7.
2. **El contenido "teórico de ejemplo" está mal copiado/genérico.** En las prácticas 3 a 7, la sección "Ejemplo del procedimiento de diseño → Fundamento Teórico / Procedimiento / Referencias" es literalmente el mismo texto sobre un **sensor infrarrojo y un servomotor con Arduino**, que no tiene relación con el tema real de la práctica (detección de formas, fotomatón, lector de códigos de barras, reconocimiento facial, etc.). Es evidente que ese bloque se copió y pegó sin adaptarlo — es la prueba más clara de que el material "está muy simple" / poco elaborado.
3. **Secciones vacías.** "Archivos proporcionados" y "Cuestionario" aparecen como encabezados sin contenido en las 7 prácticas — el material está incompleto.
4. **No hay enfoque de reconocimiento de patrones "real" (matemático/algorítmico).** El programa sintético de la materia promete cosas como extracción y clasificación de características, biometría, huellas dactilares, iris, sistemas multibiométricos — pero las 7 prácticas del Notion solo cubren manejo de una GUI ya hecha en .NET, sin tocar los fundamentos (procesamiento digital de imágenes, extracción de características, clasificadores, dominio de frecuencia, etc.) que si se plantean en la descripción del curso.

**Por eso tiene sentido lo que pidió el ingeniero:** complementar cada práctica con una implementación equivalente en **Python** (p. ej. usando `OpenCV`, `numpy`, `scikit-image` o `scikit-learn` según el caso) que reproduzca el mismo objetivo de la práctica original pero mostrando el proceso real de reconocimiento de patrones (código, algoritmo, explicación técnica), en vez de solo ejecutar un `.exe` y tomar capturas. Esto da:
- Evidencia real de comprensión del algoritmo (no solo de manejo de una GUI ajena).
- Portabilidad (no depende de Windows/.NET ni de tener el `.exe` original).
- Contenido más alineado al propósito real de la unidad de aprendizaje (extracción/clasificación de características, no solo demos visuales).

**Sugerencia de mapeo práctica → posible enfoque en Python** (a definir con el profesor antes de implementar):

| Práctica | Tema AForge original | Posible equivalente en Python |
|---|---|---|
| 1 | Detección y seguimiento de color | OpenCV: segmentación por color (HSV) + tracking (ej. `cv2.CamShift`/`cv2.Tracker`) |
| 2 | Parámetros de imagen (brillo/contraste/saturación) | OpenCV/`PIL`: transformaciones de brillo-contraste, ecualización de histograma |
| 3 | Detección de movimiento | OpenCV: diferencia de frames / sustracción de fondo (`cv2.createBackgroundSubtractorMOG2`) |
| 4 | Detección de formas | OpenCV: detección de contornos y aproximación poligonal (`cv2.findContours`, `cv2.approxPolyDP`) |
| 5 | Fotomatón (edición de imágenes) | OpenCV/`PIL`: filtros, superposición de fondos, ajustes de color |
| 6 | Lector de código de barras | `pyzbar` + OpenCV para lectura y decodificación de códigos de barras |
| 7 | Reconocimiento/movimiento de rostro | OpenCV Haar Cascades o `face_recognition`/`mediapipe` para detección facial |

Esta tabla es una propuesta de trabajo, no parte del contenido oficial del Notion — habría que confirmarla con el ingeniero antes de desarrollarla.
