"""Puente entre la interfaz y las operaciones de ``src.core``.

Reemplaza a la antigua capa web (servidor HTTP + ``app.js``): recibe el texto
de los campos, llama al núcleo y devuelve un resultado listo para mostrar.
No importa tkinter, por lo que se puede probar sin entorno gráfico.
"""

from dataclasses import dataclass

from src.core.multiplication import multiply_by_addition
from src.core.roman import add_roman

ERROR_TITLE = "Revisa los datos"
DIGIT_ERROR = "Los dos factores deben ser dígitos enteros entre 0 y 9."


@dataclass(frozen=True)
class Outcome:
    """Texto que la interfaz debe mostrar en un panel de resultado."""

    value: str
    detail: str
    is_error: bool = False


def _error(message: str) -> Outcome:
    return Outcome(ERROR_TITLE, message, is_error=True)


def roman_sum(first: str, second: str) -> Outcome:
    """Suma dos numerales romanos escritos como texto."""
    try:
        total, numeral = add_roman(first, second)
    except ValueError as error:
        return _error(str(error))
    detail = f"{first.strip().upper()} + {second.strip().upper()} = {total}"
    return Outcome(numeral, detail)


def multiplication(multiplicand_text: str, multiplier_text: str) -> Outcome:
    """Multiplica dos dígitos escritos como texto mediante sumas repetidas."""
    try:
        multiplicand = int(multiplicand_text.strip())
        multiplier = int(multiplier_text.strip())
    except ValueError:
        return _error(DIGIT_ERROR)

    try:
        total, partial_sums = multiply_by_addition(multiplicand, multiplier)
    except ValueError as error:
        return _error(str(error))

    if partial_sums:
        repeated = " + ".join([str(multiplicand)] * multiplier)
    else:
        repeated = "sin sumas (factor cero)"
    return Outcome(str(total), f"{multiplicand} × {multiplier} = {repeated}")
