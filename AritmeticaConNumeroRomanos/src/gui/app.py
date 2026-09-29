"""Ventana principal de la aplicación (equivalente al antiguo ``index.html``)."""

import sys
import tkinter as tk

from src.gui.calculations import multiplication, roman_sum
from src.gui.theme import GREEN, INK, LINE, MUTED, ORANGE, PAPER, Fonts
from src.gui.widgets import Divider, FlatButton, LabeledEntry, ResultPanel

CONVERSIONS = (
    (1, "I"), (4, "IV"), (5, "V"), (9, "IX"), (10, "X"), (40, "XL"), (50, "L"),
    (90, "XC"), (100, "C"), (400, "CD"), (500, "D"), (900, "CM"), (1000, "M"),
)  # fmt: skip

SIDE_MARGIN = 48


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Aritmética romana")
        self.configure(bg=PAPER)
        self.geometry("1060x800")
        self.minsize(940, 760)
        self.fonts = Fonts(self)

        self._build_topbar()
        self._build_footer()
        main = tk.Frame(self, bg=PAPER)
        main.pack(side="top", fill="both", expand=True, padx=SIDE_MARGIN)
        self._build_intro(main)
        self._build_workbench(main)

    # ---- Barra superior y pie -------------------------------------------------

    def _build_topbar(self) -> None:
        bar = tk.Frame(self, bg=PAPER)
        bar.pack(side="top", fill="x")
        row = tk.Frame(bar, bg=PAPER)
        row.pack(fill="x", padx=SIDE_MARGIN, pady=16)
        for column in range(3):
            row.columnconfigure(column, weight=1, uniform="topbar")

        wordmark = tk.Frame(row, bg=PAPER)
        wordmark.grid(row=0, column=0, sticky="w")
        tk.Label(wordmark, text="AR", bg=PAPER, fg=INK, font=self.fonts.wordmark).pack(side="left")
        tk.Label(wordmark, text=".", bg=PAPER, fg=ORANGE, font=self.fonts.wordmark).pack(side="left")

        tk.Label(
            row, text="Laboratorio de operaciones · 01", bg=PAPER, fg=MUTED, font=self.fonts.mono_small
        ).grid(row=0, column=1)

        status = tk.Frame(row, bg=PAPER)
        status.grid(row=0, column=2, sticky="e")
        tk.Label(status, text="●", bg=PAPER, fg=GREEN, font=self.fonts.mono_small).pack(side="left")
        tk.Label(
            status, text=" LISTO PARA CALCULAR", bg=PAPER, fg=GREEN, font=self.fonts.mono_small
        ).pack(side="left")
        Divider(bar).pack(fill="x")

    def _build_footer(self) -> None:
        footer = tk.Frame(self, bg=PAPER)
        footer.pack(side="bottom", fill="x")
        Divider(footer).pack(fill="x")
        row = tk.Frame(footer, bg=PAPER)
        row.pack(fill="x", padx=SIDE_MARGIN, pady=18)
        for column in range(3):
            row.columnconfigure(column, weight=1, uniform="footer")
        font = self.fonts.mono_small
        tk.Label(row, text="ARITMÉTICA ELEMENTAL", bg=PAPER, fg=MUTED, font=font).grid(row=0, column=0, sticky="w")
        tk.Label(row, text="SUMAR ES REPETIR.", bg=PAPER, fg=GREEN, font=font).grid(row=0, column=1)
        tk.Label(row, text="MMXXVI", bg=PAPER, fg=MUTED, font=font).grid(row=0, column=2, sticky="e")

    # ---- Introducción -----------------------------------------------------------

    def _build_intro(self, parent: tk.Misc) -> None:
        intro = tk.Frame(parent, bg=PAPER)
        intro.pack(fill="x")
        fonts = self.fonts

        tk.Label(
            intro, text="DOS REGLAS. UNA OPERACIÓN A LA VEZ.", bg=PAPER, fg=ORANGE, font=fonts.mono_small, anchor="w"
        ).pack(fill="x", pady=(44, 16))
        tk.Label(intro, text="Aritmética con", bg=PAPER, fg=INK, font=fonts.h1, anchor="w").pack(fill="x")
        tk.Label(intro, text="números romanos.", bg=PAPER, fg=GREEN, font=fonts.h1_em, anchor="w").pack(fill="x")
        tk.Label(
            intro,
            text="Suma con símbolos romanos. Multiplica como se hacía antes: sumando una y otra vez.",
            bg=PAPER,
            fg=MUTED,
            font=fonts.intro_copy,
            anchor="w",
            justify="left",
            wraplength=405,
        ).pack(fill="x", pady=(18, 40))

        mark = tk.Frame(intro, bg=PAPER)
        tk.Label(mark, text="I", bg=PAPER, fg=GREEN, font=fonts.index_mark).pack()
        tk.Label(mark, text="—", bg=PAPER, fg=ORANGE, font=fonts.index_dash).pack()
        tk.Label(mark, text="II", bg=PAPER, fg=GREEN, font=fonts.index_mark).pack()
        mark.place(relx=1.0, rely=1.0, anchor="se", y=-34)

        Divider(parent).pack(fill="x")

    # ---- Zona de trabajo ---------------------------------------------------------

    def _build_workbench(self, parent: tk.Misc) -> None:
        bench = tk.Frame(parent, bg=PAPER)
        bench.pack(fill="both", expand=True)
        for column, weight in ((0, 4), (1, 8), (3, 9)):
            bench.columnconfigure(column, weight=weight, uniform="bench")
        bench.rowconfigure(0, weight=1)

        self._build_reference(bench).grid(row=0, column=0, sticky="nsew", padx=(0, 30))
        self._build_roman_panel(bench).grid(row=0, column=1, sticky="nsew", padx=(0, 34))
        Divider(bench, vertical=True).grid(row=0, column=2, sticky="ns")
        self._build_multiplication_panel(bench).grid(row=0, column=3, sticky="nsew", padx=(34, 0))

    def _build_reference(self, parent: tk.Misc) -> tk.Frame:
        fonts = self.fonts
        panel = tk.Frame(parent, bg=PAPER)
        tk.Label(
            panel, text="Conversiones comunes", bg=PAPER, fg=ORANGE, font=fonts.mono_tiny, anchor="w"
        ).pack(fill="x", pady=(30, 10))
        tk.Label(
            panel, text="Enteros a romanos", bg=PAPER, fg=INK, font=fonts.h2_small, anchor="w"
        ).pack(fill="x", pady=(0, 10))

        table = tk.Frame(panel, bg=PAPER)
        table.pack(fill="x")
        table.columnconfigure(0, weight=1)
        table.columnconfigure(1, weight=1)
        for column, title in enumerate(("Entero", "Romano")):
            tk.Label(table, text=title, bg=PAPER, fg=MUTED, font=fonts.mono_tiny, anchor="w").grid(
                row=0, column=column, sticky="w", pady=(0, 6)
            )
        Divider(table, color=INK).grid(row=1, column=0, columnspan=2, sticky="ew")
        for index, (number, numeral) in enumerate(CONVERSIONS):
            row = 2 + index * 2
            tk.Label(table, text=str(number), bg=PAPER, fg=INK, font=fonts.table_cell, anchor="w").grid(
                row=row, column=0, sticky="w", pady=4
            )
            tk.Label(table, text=numeral, bg=PAPER, fg=GREEN, font=fonts.table_cell_accent, anchor="w").grid(
                row=row, column=1, sticky="w", pady=4
            )
            Divider(table).grid(row=row + 1, column=0, columnspan=2, sticky="ew")
        return panel

    def _build_operation_header(
        self, parent: tk.Misc, index_text: str, accent: str, title: str, description: str
    ) -> None:
        fonts = self.fonts
        heading = tk.Frame(parent, bg=PAPER)
        heading.pack(fill="x", pady=(30, 0))
        tk.Label(heading, text=index_text, bg=PAPER, fg=accent, font=fonts.mono_small).pack(side="left")
        rule = Divider(heading)
        rule.pack(side="left", fill="x", expand=True, padx=(14, 0))
        tk.Label(parent, text=title, bg=PAPER, fg=INK, font=fonts.h2, anchor="w").pack(fill="x", pady=(20, 6))
        tk.Label(
            parent,
            text=description,
            bg=PAPER,
            fg=MUTED,
            font=fonts.copy,
            anchor="nw",
            justify="left",
            wraplength=380,
            height=2,
        ).pack(fill="x", pady=(0, 22))

    def _place_inputs(self, row: tk.Frame, operator: str, left: LabeledEntry, right: LabeledEntry) -> None:
        """Coloca dos campos separados por un operador; ambos deben ser hijos de ``row``."""
        row.columnconfigure(0, weight=1, uniform="inputs")
        row.columnconfigure(2, weight=1, uniform="inputs")
        left.grid(row=0, column=0, sticky="ew")
        tk.Label(row, text=operator, bg=PAPER, fg=ORANGE, font=self.fonts.operator).grid(
            row=0, column=1, sticky="s", padx=10, pady=(0, 10)
        )
        right.grid(row=0, column=2, sticky="ew")

    def _build_roman_panel(self, parent: tk.Misc) -> tk.Frame:
        panel = tk.Frame(parent, bg=PAPER)
        self._build_operation_header(
            panel, "01 / ROMANOS", GREEN, "Suma romana", "Ingresa dos numerales del I al MMMCMXCIX."
        )
        row = tk.Frame(panel, bg=PAPER)
        row.pack(fill="x")
        self.roman_first = LabeledEntry(row, "Primer número", "XIV", self.fonts, 15, self._calculate_roman)
        self.roman_second = LabeledEntry(row, "Segundo número", "IX", self.fonts, 15, self._calculate_roman)
        self._place_inputs(row, "+", self.roman_first, self.roman_second)

        FlatButton(panel, "Calcular suma", self._calculate_roman, GREEN, self.fonts).pack(fill="x", pady=(16, 0))
        self.roman_result = ResultPanel(panel, self.fonts, GREEN)
        self.roman_result.pack(fill="x", pady=(24, 0))
        return panel

    def _build_multiplication_panel(self, parent: tk.Misc) -> tk.Frame:
        panel = tk.Frame(parent, bg=PAPER)
        self._build_operation_header(
            panel,
            "02 / SUMA REPETIDA",
            ORANGE,
            "Multiplicación",
            "Solo dígitos del 0 al 9. El segundo factor indica cuántas veces sumar.",
        )
        row = tk.Frame(panel, bg=PAPER)
        row.pack(fill="x")
        self.multiplicand = LabeledEntry(row, "Primer factor", "7", self.fonts, 3, self._calculate_multiplication)
        self.multiplier = LabeledEntry(row, "Segundo factor", "4", self.fonts, 3, self._calculate_multiplication)
        self.multiplicand.enable_digit_stepper()
        self.multiplier.enable_digit_stepper()
        self._place_inputs(row, "×", self.multiplicand, self.multiplier)

        FlatButton(panel, "Ver las sumas", self._calculate_multiplication, INK, self.fonts).pack(fill="x", pady=(16, 0))
        self.multiply_result = ResultPanel(panel, self.fonts, ORANGE)
        self.multiply_result.pack(fill="x", pady=(24, 0))
        return panel

    # ---- Acciones -----------------------------------------------------------------

    def _calculate_roman(self) -> None:
        self.roman_result.show(roman_sum(self.roman_first.get(), self.roman_second.get()))

    def _calculate_multiplication(self) -> None:
        self.multiply_result.show(multiplication(self.multiplicand.get(), self.multiplier.get()))


def _enable_high_dpi() -> None:
    """En Windows evita que el sistema escale la ventana y la vuelva borrosa."""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass


def run_app() -> None:
    _enable_high_dpi()
    App().mainloop()
