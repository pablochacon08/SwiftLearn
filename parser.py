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
    'declaracion : VAR ID ASSIGN condicion'


# Reasignación de una variable ya declarada: total = total + 5, contador += 1
def p_reasignacion(p):
    'reasignacion : destino operador_asig condicion'


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

# Sentencias del aporte de Danna
def p_sentencia_danna(p):
    '''sentencia : declaracion_tipada
                 | ciclo_while
                 | control_ciclo
                 | funcion_sin_retorno
                 | impresion'''
 
 
# Declaración con anotación de tipo: var nombre: String = "Danna"
def p_declaracion_tipada(p):
    'declaracion_tipada : VAR ID COLON tipo ASSIGN expresion'
 
 
# Tipo diccionario: [String: Int]
def p_tipo_diccionario(p):
    'tipo : LBRACKET ID COLON ID RBRACKET'
 
 
# Estructura de control while: while contador < 10 { contador += 1 }
def p_ciclo_while(p):
    'ciclo_while : WHILE condicion LBRACE programa RBRACE'
 
 
# Control del ciclo: break y continue
def p_control_ciclo(p):
    '''control_ciclo : BREAK
                     | CONTINUE'''
 
 
# Función sin retorno con parámetros: func saludar(nombre: String) { ... }
def p_funcion_sin_retorno(p):
    'funcion_sin_retorno : FUNC ID LPAREN parametros RPAREN LBRACE programa RBRACE'
 
 
# Impresión de uno o varios valores: print("Hola", nombre)
def p_impresion(p):
    '''impresion : PRINT LPAREN elementos RPAREN
                 | PRINT LPAREN RPAREN'''
 
 
# Nuevos valores: cadenas de texto y diccionarios
def p_valor_danna(p):
    '''valor : STRING
             | diccionario'''
 
 
# Diccionario con pares clave: valor, o vacío: ["Danna": 21, "Pablo": 17], [:]
def p_diccionario(p):
    '''diccionario : LBRACKET pares RBRACKET
                   | LBRACKET COLON RBRACKET'''
 
 
# Pares clave: valor separados por comas
def p_pares(p):
    '''pares : par
             | pares COMMA par'''
 
 
# Par clave: valor
def p_par(p):
    'par : expresion COLON expresion'
 
# ===== Fin aporte Danna Ayala =====


# ===== Inicio aporte Jack Vera =====
# Reglas: constantes con let, expresiones booleanas, ciclo for-in,
# tuplas, función sin parámetros y lectura de datos con readLine

# Precedencia de los operadores lógicos, de menor a mayor prioridad.
# Se agregan antes de la tabla de Pablo para que primero se evalúe el !,
# luego el && y al final el ||
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
) + precedence


# Sentencias que se agregan con este aporte
def p_sentencia_jack(p):
    '''sentencia : declaracion_constante
                 | declaracion_constante_tipada
                 | ciclo_for
                 | funcion_sin_parametros
                 | sentencia SEMICOLON'''


# Declaración de una constante: let pi = 3.14
def p_declaracion_constante(p):
    'declaracion_constante : LET ID ASSIGN expresion'


# Declaración de una constante indicando su tipo: let nombre: String = "Jack"
def p_declaracion_constante_tipada(p):
    'declaracion_constante_tipada : LET ID COLON tipo ASSIGN expresion'


# Se amplía la condición para poder unir varias con &&, || y negarlas con !
# Por ejemplo: edad >= 18 && activo || !bloqueado
def p_condicion_logica(p):
    '''condicion : condicion AND condicion
                 | condicion OR condicion
                 | NOT condicion'''


# Condición dentro de paréntesis: esAdmin || (edad >= 18 && !bloqueado)
def p_condicion_parentesis(p):
    'condicion : LPAREN condicion RPAREN'


# Permite usar una sola variable como condición: if activo { ... }
def p_condicion_expresion(p):
    'condicion : expresion'


# Ciclo for-in para recorrer una lista: for numero in numeros { ... }
def p_ciclo_for(p):
    'ciclo_for : FOR ID IN expresion LBRACE programa RBRACE'


# Función que no recibe parámetros: func mostrar() { ... }
def p_funcion_sin_parametros(p):
    'funcion_sin_parametros : FUNC ID LPAREN RPAREN LBRACE programa RBRACE'


# Valores nuevos: true, false, nil, tuplas y readLine()
def p_valor_jack(p):
    '''valor : TRUE
             | FALSE
             | NIL
             | tupla
             | lectura'''


# Tupla de dos o más valores, que pueden ser de distinto tipo: (3, 4), ("Ana", 20)
def p_tupla(p):
    'tupla : LPAREN expresion COMMA elementos RPAREN'


# Lectura de un dato ingresado por teclado: readLine()
def p_lectura(p):
    'lectura : READLINE LPAREN RPAREN'

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
