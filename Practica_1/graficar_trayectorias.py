"""
Lee logs/trayectoria.csv (generado por deteccion_color.py) y grafica la
trayectoria (posicion X vs Y) de cada objeto probado, para usarla como evidencia
grafica en el reporte de la practica.
"""

import argparse
import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

# Paleta categorica (orden fijo, seguro para daltonismo) - primeros 3 tonos
# validan comparaciones todas-contra-todas, ideal para pocas series como esta.
PALETA = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

SUPERFICIE = "#fcfcfb"
TINTA_PRIMARIA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
TINTA_MUTED = "#898781"
GRID = "#e1e0d9"
EJE = "#c3c2b7"


def parse_args():
    parser = argparse.ArgumentParser(description="Grafica las trayectorias registradas en trayectoria.csv")
    parser.add_argument(
        "--csv", default=None,
        help="Ruta al CSV de entrada (default: logs/trayectoria.csv junto a este script)",
    )
    parser.add_argument(
        "--out", default=None,
        help="Ruta de salida del PNG (default: capturas/trayectorias.png junto a este script)",
    )
    return parser.parse_args()


def cargar_trayectorias(csv_path):
    trayectorias = defaultdict(list)
    with open(csv_path, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            trayectorias[fila["objeto"]].append((int(fila["cx"]), int(fila["cy"])))
    return trayectorias


def graficar(trayectorias, out_path):
    fig, ax = plt.subplots(figsize=(8, 6), facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    for i, (objeto, puntos) in enumerate(trayectorias.items()):
        color = PALETA[i % len(PALETA)]
        xs = [p[0] for p in puntos]
        ys = [p[1] for p in puntos]
        ax.plot(xs, ys, color=color, linewidth=2, label=objeto, zorder=3)
        ax.scatter(xs[0], ys[0], color=color, marker="o", s=45, zorder=4)   # inicio
        ax.scatter(xs[-1], ys[-1], color=color, marker="s", s=45, zorder=4)  # fin

    ax.set_title("Trayectorias detectadas - Práctica 1", color=TINTA_PRIMARIA, fontsize=13, pad=12)
    ax.set_xlabel("Posición X (px)", color=TINTA_SECUNDARIA)
    ax.set_ylabel("Posición Y (px)", color=TINTA_SECUNDARIA)

    # El origen de pixeles en OpenCV crece hacia abajo; invertimos Y para que
    # la grafica se lea igual que la imagen de la camara.
    ax.invert_yaxis()

    ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    for spine in ax.spines.values():
        spine.set_color(EJE)
    ax.tick_params(colors=TINTA_MUTED)

    ax.legend(frameon=False, labelcolor=TINTA_PRIMARIA, loc="best")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, facecolor=SUPERFICIE)
    print(f"Grafica guardada en: {out_path}")


def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = args.csv or os.path.join(base_dir, "logs", "trayectoria.csv")
    out_path = args.out or os.path.join(base_dir, "capturas", "trayectorias.png")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"No se encontro {csv_path}. Ejecuta primero deteccion_color.py y guarda algunas capturas."
        )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    trayectorias = cargar_trayectorias(csv_path)
    if not trayectorias:
        raise ValueError("El CSV no tiene registros de trayectoria todavia.")

    graficar(trayectorias, out_path)


if __name__ == "__main__":
    main()
