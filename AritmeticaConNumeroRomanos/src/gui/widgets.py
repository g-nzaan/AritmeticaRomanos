"""Widgets personalizados con el estilo visual de la aplicación."""

import tkinter as tk
from collections.abc import Callable

from src.gui.calculations import Outcome
from src.gui.theme import (
    FIELD,
    FIELD_FOCUS,
    GREEN,
    INK,
    LINE,
    MUTED,
    ORANGE,
    PAPER,
    WHITE,
    Fonts,
)


class Divider(tk.Frame):
    """Línea fina horizontal o vertical."""

    def __init__(self, master: tk.Misc, color: str = LINE, vertical: bool = False) -> None:
        if vertical:
            super().__init__(master, bg=color, width=1)
        else:
            super().__init__(master, bg=color, height=1)


class FlatButton(tk.Frame):
    """Botón plano de color sólido.

    ``tk.Button`` ignora los colores en macOS, así que se dibuja con un marco
    y dos etiquetas para que se vea igual en todos los sistemas.
    """

    def __init__(
        self,
        master: tk.Misc,
        text: str,
        command: Callable[[], None],
        background: str,
        fonts: Fonts,
        hover: str = ORANGE,
    ) -> None:
        super().__init__(
            master,
            bg=background,
            cursor="hand2",
            takefocus=True,
            highlightthickness=2,
            highlightbackground=PAPER,
            highlightcolor=ORANGE,
        )
        self._command = command
        self._background = background
        self._hover = hover

        self._label = tk.Label(self, text=text, bg=background, fg=WHITE, font=fonts.button)
        self._arrow = tk.Label(self, text="↗", bg=background, fg=WHITE, font=fonts.button)
        self._label.pack(side="left", padx=(15, 0), pady=13)
        self._arrow.pack(side="right", padx=(0, 15))

        for widget in (self, self._label, self._arrow):
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", lambda _event: self._paint(self._hover))
            widget.bind("<Leave>", lambda _event: self._paint(self._background))
        self.bind("<Return>", self._on_key)
        self.bind("<space>", self._on_key)

    def _paint(self, color: str) -> None:
        for widget in (self, self._label, self._arrow):
            widget.configure(bg=color)

    def _on_click(self, _event: tk.Event) -> None:
        self.focus_set()
        self._command()

    def _on_key(self, _event: tk.Event) -> str:
        self._command()
        return "break"


class LabeledEntry(tk.Frame):
    """Campo de texto con etiqueta superior, borde que resalta al enfocar y límite de longitud."""

    def __init__(
        self,
        master: tk.Misc,
        label: str,
        initial: str,
        fonts: Fonts,
        max_length: int,
        on_submit: Callable[[], None],
    ) -> None:
        super().__init__(master, bg=PAPER)
        tk.Label(self, text=label, bg=PAPER, fg=MUTED, font=fonts.mono_small, anchor="w").pack(fill="x")

        self.variable = tk.StringVar(value=initial)
        limit = self.register(lambda proposed: len(proposed) <= max_length)
        self.entry = tk.Entry(
            self,
            textvariable=self.variable,
            font=fonts.field,
            width=6,
            relief="flat",
            bd=10,
            bg=FIELD,
            fg=INK,
            insertbackground=INK,
            highlightthickness=1,
            highlightbackground=LINE,
            highlightcolor=GREEN,
            validate="key",
            validatecommand=(limit, "%P"),
        )
        self.entry.pack(fill="x", pady=(9, 0), ipady=7)
        self.entry.bind("<FocusIn>", lambda _event: self.entry.configure(bg=FIELD_FOCUS))
        self.entry.bind("<FocusOut>", lambda _event: self.entry.configure(bg=FIELD))
        self.entry.bind("<Return>", lambda _event: on_submit())

    def get(self) -> str:
        return self.variable.get()

    def enable_digit_stepper(self, minimum: int = 0, maximum: int = 9) -> None:
        """Permite subir y bajar el valor con las flechas del teclado (como un campo numérico)."""

        def step(delta: int) -> str:
            try:
                current = int(self.variable.get())
            except ValueError:
                current = minimum
            self.variable.set(str(min(maximum, max(minimum, current + delta))))
            self.entry.icursor("end")
            return "break"

        self.entry.bind("<Up>", lambda _event: step(1))
        self.entry.bind("<Down>", lambda _event: step(-1))


class ResultPanel(tk.Frame):
    """Zona de resultado: valor destacado y detalle de la operación."""

    def __init__(self, master: tk.Misc, fonts: Fonts, accent: str) -> None:
        super().__init__(master, bg=PAPER)
        self._fonts = fonts
        self._accent = accent

        Divider(self).pack(fill="x")
        tk.Label(self, text="RESULTADO", bg=PAPER, fg=MUTED, font=fonts.mono_small, anchor="w").pack(
            fill="x", pady=(15, 0)
        )
        self._value = tk.Label(
            self, text="—", bg=PAPER, fg=accent, font=fonts.result_value, anchor="w", justify="left"
        )
        self._value.pack(fill="x", pady=(7, 3))
        self._detail = tk.Label(
            self,
            text="",
            bg=PAPER,
            fg=MUTED,
            font=fonts.result_detail,
            anchor="nw",
            justify="left",
            height=2,
            wraplength=300,
        )
        self._detail.pack(fill="x")
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event: tk.Event) -> None:
        self._detail.configure(wraplength=max(event.width - 4, 120))

    def show(self, outcome: Outcome) -> None:
        if outcome.is_error:
            self._value.configure(text=outcome.value, fg=ORANGE, font=self._fonts.result_error)
        else:
            self._value.configure(text=outcome.value, fg=self._accent, font=self._fonts.result_value)
        self._detail.configure(text=outcome.detail)
