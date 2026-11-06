# ============================================================
# SwiftLearn - Analizador sintáctico para un subconjunto de Swift
# Proyecto de Lenguajes de Programación - ESPOL
# Herramienta: PLY (módulo yacc)
#
# Uso:
#   python parser.py <ruta_algoritmo.swift> <usuarioGit>
#   Ejemplo: python parser.py algoritmos/algoritmo1.swift pablochacon08
# ============================================================

import os
import sys
from datetime import datetime

import ply.yacc as yacc

import lexer as analizador_lexico
from lexer import tokens

# Lista de errores sintácticos encontrados (se escribe en el log)
errores = []


# ===== Inicio aporte Pablo Chacón =====
# Reglas: declaración con var, expresiones aritméticas, if-else,
# arreglos, función con retorno, reasignación y llamada a funciones

# Precedencia de operadores aritméticos (de menor a mayor)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
)


# Sentencias del aporte de Pablo
def p_sentencia_pablo(p):
    '''sentencia : declaracion
                 | if_else
                 | funcion
                 | retorno
                 | reasignacion
                 | llamada'''


# Declaración de variable: var total = 5 + 3
def p_declaracion(p):
    'declaracion : VAR ID ASSIGN expresion'


# Reasignación de una variable ya declarada: total = total + 5, contador += 1
def p_reasignacion(p):
    'reasignacion : destino operador_asig expresion'


# Lo que puede ir a la izquierda: una variable o un elemento del arreglo
def p_destino(p):
    '''destino : ID
               | acceso'''


# Operadores de asignación
def p_operador_asig(p):
    '''operador_asig : ASSIGN
                     | PLUS_ASSIGN
                     | MINUS_ASSIGN
                     | TIMES_ASSIGN
                     | DIVIDE_ASSIGN
                     | MOD_ASSIGN'''


# Estructura de control if, con else opcional
def p_if_else(p):
    '''if_else : IF condicion LBRACE programa RBRACE
               | IF condicion LBRACE programa RBRACE ELSE LBRACE programa RBRACE'''


# Función con retorno: func sumar(a: Int, b: Int) -> Int { ... }
def p_funcion(p):
    'funcion : FUNC ID LPAREN parametros RPAREN ARROW tipo LBRACE programa RBRACE'


# Lista de parámetros separados por comas
def p_parametros(p):
    '''parametros : parametro
                  | parametros COMMA parametro'''


# Parámetro con su tipo: a: Int
def p_parametro(p):
    'parametro : ID COLON tipo'


# Tipo de dato: Int, Double o arreglo como [Double]
def p_tipo(p):
    '''tipo : ID
            | LBRACKET ID RBRACKET'''


# Sentencia return con su valor
def p_retorno(p):
    'retorno : RETURN expresion'


# Condición simple: compara dos expresiones
def p_condicion(p):
    'condicion : expresion comparador expresion'


# Operadores de comparación
def p_comparador(p):
    '''comparador : EQ
                  | NE
                  | LT
                  | GT
                  | LE
                  | GE'''


# Expresión aritmética con uno o más operadores
def p_expresion(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion
                 | expresion MOD expresion
                 | LPAREN expresion RPAREN
                 | valor'''


# Valores que pueden formar una expresión
def p_valor(p):
    '''valor : INT
             | DOUBLE
             | ID
             | arreglo
             | acceso
             | llamada'''


# Arreglo: [8.5, 9.0, 6.5]
def p_arreglo(p):
    'arreglo : LBRACKET elementos RBRACKET'


# Elementos del arreglo separados por comas
def p_elementos(p):
    '''elementos : expresion
                 | elementos COMMA expresion'''


# Acceso a un elemento del arreglo: notas[0]
def p_acceso(p):
    'acceso : ID LBRACKET expresion RBRACKET'


# Llamada a una función: sumar(a: 1, b: 2), saludar()
def p_llamada(p):
    '''llamada : ID LPAREN RPAREN
               | ID LPAREN argumentos RPAREN'''


# Argumentos de la llamada separados por comas
def p_argumentos(p):
    '''argumentos : argumento
                  | argumento COMMA argumentos'''


# Argumento con etiqueta (a: 1) o sin etiqueta (1)
def p_argumento(p):
    '''argumento : ID COLON expresion
                 | expresion'''

# ===== Fin aporte Pablo Chacón =====


# ===== Inicio aporte Danna Ayala =====
# Reglas: declaración con anotación de tipo, while, diccionarios,
# función sin retorno con parámetros e impresión con print

# ===== Fin aporte Danna Ayala =====


# ===== Inicio aporte Jack Vera =====
# Reglas: declaración de constantes con let, expresiones booleanas,
# for-in, tuplas, función sin parámetros y lectura con readLine

# ===== Fin aporte Jack Vera =====


# ===== Base común del analizador =====

# Regla padre: un programa es una o varias sentencias.
# Cada integrante agrega sus sentencias con su propia función p_sentencia_...
def p_programa(p):
    '''programa : sentencia
                | programa sentencia'''


# Error sintáctico: se guarda el mensaje y se continúa con el análisis
def p_error(p):
    if p:
        errores.append(f"Error sintáctico en la línea {p.lineno}: "
                       f"no se esperaba '{p.value}'. Revisa la instrucción "
                       f"antes de este símbolo.")
    else:
        errores.append("Error sintáctico al final del archivo: la última "
                       "instrucción está incompleta. Revisa que no falte "
                       "una llave, un paréntesis o un valor.")


# La regla padre es programa, aunque los aportes estén escritos antes
start = 'programa'

parser = yacc.yacc()


def analizar(ruta_algoritmo, usuario):
    """Analiza un archivo Swift y guarda el log en la carpeta logs/."""
    with open(ruta_algoritmo, encoding='utf-8') as archivo:
        codigo = archivo.read()

    errores.clear()
    analizador_lexico.lexer.lineno = 1
    parser.parse(codigo, lexer=analizador_lexico.lexer)

    ahora = datetime.now()
    nombre_log = (f"sintactico-{usuario}-"
                  f"{ahora.strftime('%d%m%Y')}-{ahora.strftime('%Hh%M')}.txt")
    os.makedirs('logs', exist_ok=True)
    ruta_log = os.path.join('logs', nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write("ANÁLISIS SINTÁCTICO - SwiftLearn\n")
        log.write(f"Archivo: {ruta_algoritmo}\n")
        log.write(f"Desarrollador: {usuario}\n")
        log.write(f"Fecha: {ahora.strftime('%d-%m-%Y %H:%M')}\n\n")
        log.write(f"ERRORES SINTÁCTICOS ({len(errores)})\n")
        log.write("\n".join(errores) if errores else "Sin errores sintácticos.")
        log.write("\n")

    print(f"Errores sintácticos: {len(errores)}")
    for error in errores:
        print(f"  {error}")
    print(f"Log generado: {ruta_log}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python parser.py <ruta_algoritmo.swift> <usuarioGit>")
        sys.exit(1)
    analizar(sys.argv[1], sys.argv[2])
