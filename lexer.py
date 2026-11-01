# ============================================================
# SwiftLearn - Analizador léxico para un subconjunto de Swift
# Proyecto de Lenguajes de Programación - ESPOL
# Herramienta: PLY (módulo lex)
#
# Uso:
#   python lexer.py <ruta_algoritmo.swift> <NombreApellido>
#   Ejemplo: python lexer.py algoritmos/algoritmo1.swift PabloChacon
# ============================================================

import os
import sys
from datetime import datetime

import ply.lex as lex

# Cada integrante agrega sus palabras reservadas a este diccionario
# y sus tokens a esta lista, dentro de su bloque.
reserved = {}
tokens = []

# Lista de errores léxicos encontrados (se escribe en el log)
errores = []


# ===== Inicio aporte Pablo Chacón =====

# Palabras reservadas: declaración de variables, condicionales y funciones
reserved.update({
    'var': 'VAR',
    'if': 'IF',
    'else': 'ELSE',
    'func': 'FUNC',
    'return': 'RETURN',
})

tokens += [
    'ID',        # identificadores
    'DOUBLE',    # números decimales
    'INT',       # números enteros
    'PLUS',      # +
    'MINUS',     # -
    'TIMES',     # *
    'DIVIDE',    # /
    'MOD',       # %
    'LBRACKET',  # [
    'RBRACKET',  # ]
    'ARROW',     # ->
]

# Operadores aritméticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'

# Delimitadores
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ARROW = r'->'


# Número decimal: va antes que INT para que 3.14 no se separe en 3 y .14
def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


# Número entero
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Identificador: si coincide con una palabra reservada, toma ese tipo
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# ===== Fin aporte Pablo Chacón =====


# ===== Inicio aporte Danna Ayala =====
# Tokens: while, break, continue, cadenas de texto,
# operadores de comparación, { }, : y comentarios

# Palabras reservadas: ciclo while y control del ciclo
reserved.update({
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
})

tokens += [
    'STRING',    # cadenas de texto "..."
    'EQ',        # ==
    'NE',        # !=
    'LE',        # <=
    'GE',        # >=
    'LT',        # <
    'GT',        # >
    'LBRACE',    # {
    'RBRACE',    # }
    'COLON',     # :
]

# Operadores de comparación
# PLY ordena las reglas de texto de mayor a menor longitud,
# por eso <= se reconoce antes que < y == antes que =
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'

# Delimitadores de bloque y separador de tipo / clave-valor
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'


# Cadena de texto entre comillas dobles, admite secuencias como \n o \"
def t_STRING(t):
    r'"([^"\\\n]|\\.)*"'
    return t


# Comentario de varias líneas /* ... */
# Se descarta, pero se cuentan sus saltos de línea para no perder la numeración
def t_COMMENT_MULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


# Comentario de una línea // ...
# Se descarta. Al ser función, PLY lo revisa antes que t_DIVIDE
def t_COMMENT(t):
    r'//.*'
# ===== Fin aporte Danna Ayala =====


# ===== Inicio aporte Jack Vera =====
# Tokens: let, for, in, true, false, nil,
# operadores lógicos y de asignación, ( ), la coma y ;

# Palabras reservadas: constantes, ciclos y valores especiales
reserved.update({
    'let': 'LET',
    'for': 'FOR',
    'in': 'IN',
    'true': 'TRUE',
    'false': 'FALSE',
    'nil': 'NIL',
})

tokens += [
    'LPAREN',    # (
    'RPAREN',    # )
    'COMMA',     # ,
    'SEMICOLON', # ;
    'ASSIGN',    # =
    'PLUS_ASSIGN',   # +=
    'MINUS_ASSIGN',  # -=
    'TIMES_ASSIGN',  # *=
    'DIVIDE_ASSIGN', # /=
    'MOD_ASSIGN',    # %=
    'AND',       # &&
    'OR',        # ||
    'NOT',       # !
]

# Operadores de asignación compuesta, primero los más largos
# para que PLY no los separe como operador + y asignación =
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_ASSIGN = r'='

# Operadores lógicos
# El lexer descarta los comentarios antes de reconocer el operador /
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# Separadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'

# ===== Fin aporte Jack Vera =====


# ===== Base común del analizador =====

# Las palabras reservadas también son tokens
tokens += list(reserved.values())

# Espacios y tabulaciones se ignoran
t_ignore = ' \t'


# Cuenta los saltos de línea para saber en qué línea está cada token
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def columna(token):
    inicio_linea = token.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
    return token.lexpos - inicio_linea + 1


# Error léxico: mensaje educativo y se continúa con el siguiente carácter
def t_error(t):
    caracter = t.value[0]
    mensaje = (f"Error léxico en la línea {t.lineno}, columna {columna(t)}: "
               f"el carácter '{caracter}' no pertenece al lenguaje Swift. "
               f"Revisa si es un error de escritura o elimínalo.")
    errores.append(mensaje)
    t.lexer.skip(1)


lexer = lex.lex()


def analizar(ruta_algoritmo, autor):
    """Analiza un archivo Swift y guarda el log en la carpeta logs/."""
    with open(ruta_algoritmo, encoding='utf-8') as archivo:
        codigo = archivo.read()

    errores.clear()
    lexer.lineno = 1
    lexer.input(codigo)

    lineas_tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        lineas_tokens.append(
            f"Línea {tok.lineno:<4} {tok.type:<12} {tok.value}")

    ahora = datetime.now()
    nombre_log = f"lexico-{autor}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    os.makedirs('logs', exist_ok=True)
    ruta_log = os.path.join('logs', nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write("ANÁLISIS LÉXICO - SwiftLearn\n")
        log.write(f"Archivo: {ruta_algoritmo}\n")
        log.write(f"Desarrollador: {autor}\n")
        log.write(f"Fecha: {ahora.strftime('%d-%m-%Y %H:%M')}\n\n")
        log.write(f"TOKENS RECONOCIDOS ({len(lineas_tokens)})\n")
        log.write("\n".join(lineas_tokens) + "\n\n")
        log.write(f"ERRORES LÉXICOS ({len(errores)})\n")
        log.write("\n".join(errores) if errores else "Sin errores léxicos.")
        log.write("\n")

    print(f"Tokens reconocidos: {len(lineas_tokens)}")
    print(f"Errores léxicos: {len(errores)}")
    print(f"Log generado: {ruta_log}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python lexer.py <ruta_algoritmo.swift> <NombreApellido>")
        sys.exit(1)
    analizar(sys.argv[1], sys.argv[2])
    