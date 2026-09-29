ROMAN_VALUES = (
    ("M", 1000),
    ("CM", 900),
    ("D", 500),
    ("CD", 400),
    ("C", 100),
    ("XC", 90),
    ("L", 50),
    ("XL", 40),
    ("X", 10),
    ("IX", 9),
    ("V", 5),
    ("IV", 4),
    ("I", 1),
)
MAX_ROMAN_VALUE = 3999


def to_roman(number: int) -> str:
    if isinstance(number, bool) or not 1 <= number <= MAX_ROMAN_VALUE:
        raise ValueError("El número debe estar entre 1 y 3999 para expresarse en romano.")

    numeral = []
    for symbol, value in ROMAN_VALUES:
        count, number = divmod(number, value)
        numeral.append(symbol * count)
    return "".join(numeral)


def from_roman(numeral: str) -> int:
    if not isinstance(numeral, str):
        raise ValueError("Escribe un número romano válido, por ejemplo XIV.")

    normalized = numeral.strip().upper()
    if not normalized:
        raise ValueError("Escribe un número romano.")

    total = 0
    index = 0
    for symbol, value in ROMAN_VALUES:
        while normalized.startswith(symbol, index):
            total += value
            index += len(symbol)

    if index != len(normalized) or to_roman(total) != normalized:
        raise ValueError(f"{normalized} no es un número romano estándar válido.")
    return total


def add_roman(first: str, second: str) -> tuple[int, str]:
    total = from_roman(first) + from_roman(second)
    if total > MAX_ROMAN_VALUE:
        raise ValueError("La suma supera 3999, el límite de la notación romana estándar.")
    return total, to_roman(total)