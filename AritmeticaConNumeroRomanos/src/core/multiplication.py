def multiply_by_addition(multiplicand: int, multiplier: int) -> tuple[int, list[int]]:
    for value in (multiplicand, multiplier):
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 9:
            raise ValueError("Los dos factores deben ser dígitos enteros entre 0 y 9.")

    partial_sums = []
    total = 0
    for _ in range(multiplier):
        total += multiplicand
        partial_sums.append(total)
    return total, partial_sums