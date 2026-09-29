"""Paleta de colores y tipografías (equivalente al antiguo ``style.css``)."""

import tkinter as tk
from tkinter import font as tkfont

PAPER = "#f2f1e9"
INK = "#202522"
MUTED = "#73776e"
LINE = "#d4d4c8"
GREEN = "#17624d"
ORANGE = "#c45a38"
FIELD = "#f8f7f1"
FIELD_FOCUS = "#fffef9"
WHITE = "#ffffff"

# Se usa la primera familia instalada; las últimas son alias que Tk resuelve
# en cualquier sistema operativo.
_SERIF = ("Playfair Display", "Georgia", "Times New Roman", "DejaVu Serif", "Times")
_SANS = ("DM Sans", "Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans", "Helvetica")
_MONO = ("DM Mono", "Consolas", "Menlo", "Courier New", "DejaVu Sans Mono", "Courier")


def _pick(available: set[str], candidates: tuple[str, ...]) -> str:
    for name in candidates:
        if name.lower() in available:
            return name
    return candidates[-1]


class Fonts:
    """Conjunto de fuentes de la aplicación (requiere una raíz de Tk creada)."""

    def __init__(self, root: tk.Misc) -> None:
        available = {name.lower() for name in tkfont.families(root)}
        serif = _pick(available, _SERIF)
        sans = _pick(available, _SANS)
        mono = _pick(available, _MONO)

        def make(family: str, size: int, weight: str = "normal", slant: str = "roman") -> tkfont.Font:
            # Tamaño negativo = píxeles, igual que en CSS.
            return tkfont.Font(root=root, family=family, size=-size, weight=weight, slant=slant)

        self.wordmark = make(serif, 25, "bold")
        self.mono_small = make(mono, 10)
        self.mono_tiny = make(mono, 9)
        self.h1 = make(serif, 46, "bold")
        self.h1_em = make(serif, 46, "bold", "italic")
        self.intro_copy = make(sans, 14)
        self.index_mark = make(serif, 25)
        self.index_dash = make(mono, 14)
        self.h2_small = make(serif, 18, "bold")
        self.table_cell = make(mono, 11)
        self.table_cell_accent = make(mono, 11, "bold")
        self.h2 = make(serif, 28, "bold")
        self.copy = make(sans, 13)
        self.field = make(mono, 18)
        self.operator = make(serif, 21)
        self.button = make(sans, 13, "bold")
        self.result_value = make(serif, 29, "bold")
        self.result_error = make(serif, 19, "bold")
        self.result_detail = make(mono, 10)
