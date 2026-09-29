# Aritmética Romana y Multiplicación por Sumas

Aplicación de escritorio diseñada para practicar y visualizar dos operaciones aritméticas elementales:

- **Suma de números romanos**, con validación estricta de la notación romana canónica.
- **Multiplicación mediante sumas repetidas**, enfocada en factores de un solo dígito.

**Cero dependencias externas:** el proyecto está desarrollado íntegramente en Python y su biblioteca estándar. La interfaz usa `tkinter`, que ya viene incluido con Python.

> En algunas distribuciones de Linux `tkinter` se instala aparte: `sudo apt install python3-tk`.

## Uso

```
python main.py
```

- Pulsa **Enter** en cualquier campo o haz clic en el botón para calcular.
- En los campos de la multiplicación, las flechas ↑ / ↓ suben y bajan el dígito.

## Estructura

```
main.py                  Punto de entrada
src/core/                Operaciones aritméticas, independientes de la interfaz
src/gui/calculations.py  Convierte el texto de los campos en resultados para mostrar
src/gui/theme.py         Colores y tipografías
src/gui/widgets.py       Botón, campo de texto y panel de resultado
src/gui/app.py           Ventana principal
tests/                   Pruebas automatizadas
```

`src/core` y `src/gui/calculations.py` no dependen de tkinter, así que las pruebas se ejecutan sin entorno gráfico:

```
python -m unittest discover
```
