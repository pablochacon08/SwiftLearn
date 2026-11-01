# SwiftLearn

SwiftLearn es un analizador léxico, sintáctico y semántico para un subconjunto del lenguaje Swift, desarrollado en Python con PLY (Python Lex-Yacc). Tiene un enfoque educativo: además de detectar los errores, explica por qué ocurren y cómo corregirlos, a través de una interfaz gráfica.

Proyecto de la materia Lenguajes de Programación, Escuela Superior Politécnica del Litoral (ESPOL).

## Integrantes

| Integrante | Usuario GitHub | Aporte en el analizador léxico |
|---|---|---|
| Pablo Chacón | `usuario` | Palabras reservadas `var`, `if`, `else`, `func`, `return`; identificadores; números enteros y decimales; operadores aritméticos `+ - * / %`; corchetes `[ ]` y flecha `->` |
| Danna Ayala | `usuario` | Palabras reservadas `while`, `break`, `continue`; cadenas de texto; operadores de comparación `== != < > <= >=`; llaves `{ }`; dos puntos `:`; comentarios `//` y `/* */` |
| Jack Vera | `usuario` | Palabras reservadas `let`, `for`, `in`, `true`, `false`, `nil`; operadores lógicos y de asignación; paréntesis `( )`; coma `,` y punto y coma `;` |

## Requisitos

- Python 3.10 o superior
- PLY

```bash
python -m pip install ply
```

## Uso

Desde la carpeta del proyecto:

```bash
python lexer.py <ruta_algoritmo.swift> <NombreApellido>
```

Ejemplos:

```bash
python lexer.py algoritmos/algoritmo1.swift PabloChacon
python lexer.py algoritmos/algoritmo2.swift DannaAyala
python lexer.py algoritmos/algoritmo3.swift JackVera
```

Cada ejecución muestra en consola el número de tokens reconocidos y de errores léxicos, y genera un log en la carpeta `logs/`.

## Estructura del proyecto

```
SwiftLearn/
├── algoritmos/
│   ├── algoritmo1.swift   # Algoritmo de prueba de Pablo Chacón
│   ├── algoritmo2.swift   # Algoritmo de prueba de Danna Ayala
│   └── algoritmo3.swift   # Algoritmo de prueba de Jack Vera
├── logs/                  # Logs generados en cada prueba
├── lexer.py               # Analizador léxico
└── README.md
```

## Logs

Cada prueba genera un archivo con el formato:

```
lexico-NombreApellido-dd-mm-aaaa-HHhMM.txt
```

Por ejemplo: `lexico-DannaAyala-01-11-2026-15h44.txt`.

El log incluye el archivo analizado, el desarrollador, la fecha y hora, la lista de tokens reconocidos con su línea y los errores léxicos encontrados, con un mensaje que indica la línea, la columna y el carácter no válido.

## Avances

- [x] Avance 1: Analizador léxico (PLY lex)
- [ ] Avance 2: Analizador sintáctico (PLY yacc)
- [ ] Avance 3: Analizador semántico
- [ ] Interfaz gráfica