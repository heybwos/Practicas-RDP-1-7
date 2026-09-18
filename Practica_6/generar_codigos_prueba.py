"""
Genera dos codigos de barras de prueba (Code128, sin depender de internet) para
probar lector_barcode.py sin necesidad de camara ni codigos impresos. Se guardan
en imagenes/codigo_1.png e imagenes/codigo_2.png.

Ejecutar una sola vez (o cuando se quieran regenerar):
    python generar_codigos_prueba.py
"""

import os

import barcode
from barcode.writer import ImageWriter


VALOR_1 = "123456789012"
VALOR_2 = "RECPATRONES2026"


def generar(valor, ruta_sin_extension):
    codigo = barcode.get("code128", valor, writer=ImageWriter())
    ruta_guardada = codigo.save(ruta_sin_extension)
    return ruta_guardada


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base_dir, "imagenes")
    os.makedirs(carpeta, exist_ok=True)

    ruta_1 = generar(VALOR_1, os.path.join(carpeta, "codigo_1"))
    ruta_2 = generar(VALOR_2, os.path.join(carpeta, "codigo_2"))
    print(f"Codigos generados:\n  {ruta_1} (valor: {VALOR_1})\n  {ruta_2} (valor: {VALOR_2})")


if __name__ == "__main__":
    main()
