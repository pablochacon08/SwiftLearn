# SwiftLearn

SwiftLearn es un analizador léxico, sintáctico y semántico para un subconjunto del lenguaje Swift, desarrollado en Python con PLY (Python Lex-Yacc). Tiene un enfoque educativo: además de detectar los errores, explica por qué ocurren y cómo corregirlos, a través de una interfaz gráfica.

Proyecto de la materia Lenguajes de Programación, Escuela Superior Politécnica del Litoral (ESPOL).

## Integrantes

| Integrante | Usuario GitHub | Aporte en el analizador léxico |
|---|---|---|
| Pablo Chacón | `pablochacon08` | Palabras reservadas `var`, `if`, `else`, `func`, `return`; identificadores; números enteros y decimales; operadores aritméticos `+ - * / %`; corchetes `[ ]` y flecha `->` |
| Danna Ayala | `ayaladanna04` | Palabras reservadas `while`, `break`, `continue`; cadenas de texto; operadores de comparación `== != < > <= >=`; llaves `{ }`; dos puntos `:`; comentarios `//` y `/* */` |
| Jack Vera | `cevicheman` | Palabras reservadas `let`, `for`, `in`, `true`, `false`, `nil`; operadores lógicos y de asignación; paréntesis `( )`; coma `,` y punto y coma `;` |

## Requisitos

- Python 3.10 o superior
- PLY
- Tkinter (para la interfaz gráfica)

```bash
pip install ply
```

En Ubuntu / WSL, Tkinter se instala aparte:

```bash
sudo apt install python3-tk
```

> **WSL:** para que se abra la ventana de la interfaz se necesita Windows 11, que incluye WSLg (soporte de aplicaciones gráficas de Linux). En Windows 10 la interfaz no se puede mostrar desde WSL.

**macOS:** se recomienda instalar Python desde [python.org](https://www.python.org/downloads/), que ya incluye Tkinter. Si usas Homebrew, instala también Tkinter con `brew install python-tk`. Luego, desde la carpeta del proyecto:

    python3 -m pip install ply
    python3 interfaz.py

## Uso

### Interfaz gráfica

Desde la carpeta del proyecto:

```bash
python3 interfaz.py
```

1. Elige el **Usuario** (integrante) en la esquina superior derecha. Se usa para el nombre de los logs.
2. Escribe código Swift en el editor o presiona **Abrir** para cargar un archivo `.swift` (se abre en `algoritmos/`).
3. Presiona **Análisis léxico**, **Análisis sintáctico** o **Análisis semántico**. Cada análisis se ejecuta por separado y genera solo su log.
4. Revisa los resultados:
   - **Tokens**: tabla con la línea, el tipo y el valor de cada token (análisis léxico).
   - **Errores encontrados**: contadores por fase (verde si no hay errores, rojo si los hay) y una tarjeta por error con la línea, la explicación y cómo corregirlo. Al hacer clic en una tarjeta, el editor salta a esa línea.
   - Las líneas con error se resaltan en rojo claro en el editor.
   - La barra de estado indica el resultado del análisis y el nombre del log generado.
5. **Limpiar** vacía el editor y los resultados.

### Consola

```bash
python3 lexer.py <ruta_algoritmo.swift> <NombreApellido>
python3 parser.py <ruta_algoritmo.swift> <usuarioGit>
```

Ejemplos:

```bash
python3 lexer.py algoritmos/algoritmo1.swift PabloChacon
python3 parser.py algoritmos/algoritmo1_sintactico.swift pablochacon08
python3 parser.py algoritmos/algoritmo1_semantico.swift pablochacon08
```

`lexer.py` muestra el número de tokens reconocidos y de errores léxicos. `parser.py` muestra los errores sintácticos y semánticos, y genera los dos logs.

## Estructura del proyecto

```
SwiftLearn/
├── algoritmos/
│   ├── algoritmo1.swift              # Algoritmo de prueba de Pablo Chacón
│   ├── algoritmo2.swift              # Algoritmo de prueba de Danna Ayala
│   ├── algoritmo3.swift              # Algoritmo de prueba de Jack Vera
│   ├── algoritmo*_sintactico.swift   # Pruebas con errores sintácticos
│   └── algoritmo*_semantico.swift    # Pruebas con errores semánticos
├── logs/                             # Logs generados en cada prueba
├── lexer.py                          # Analizador léxico (PLY lex)
├── parser.py                         # Analizador sintáctico y semántico (PLY yacc)
├── interfaz.py                       # Interfaz gráfica (Tkinter)
└── README.md
```

## Logs

Cada análisis genera un archivo en `logs/` con el formato:

| Análisis | Formato | Ejemplo |
|---|---|---|
| Léxico | `lexico-NombreApellido-dd-mm-aaaa-HHhMM.txt` | `lexico-DannaAyala-01-11-2026-15h44.txt` |
| Sintáctico | `sintactico-usuarioGit-ddmmaaaa-HHhMM.txt` | `sintactico-pablochacon08-13112026-11h09.txt` |
| Semántico | `semantico-usuarioGit-ddmmaaaa-HHhMM.txt` | `semantico-pablochacon08-13112026-11h09.txt` |

Cada log incluye el archivo analizado, el desarrollador, la fecha y hora y los errores encontrados, con un mensaje que indica la línea del error, la explicación y una sugerencia para corregirlo. El log léxico incluye además la lista de tokens reconocidos con su línea.

## Avances

- [x] Avance 1: Analizador léxico (PLY lex)
- [x] Avance 2: Analizador sintáctico (PLY yacc)
- [x] Avance 3: Analizador semántico
- [x] Interfaz gráfica (Tkinter)
