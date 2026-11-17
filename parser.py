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

# ===== Base del analizador semántico =====
# Tabla de símbolos: guarda cada variable declarada con su tipo
tabla_simbolos = {
    'variables': {},
    'constantes': set(),    # nombres declarados con let (regla 2)
    'funciones': {},        # tipo de retorno de cada función (reglas 5 y 6)
}
 
# Lista de errores semánticos encontrados (se escribe en el log)
errores_semanticos = []


# ===== Inicio aporte Pablo Chacón =====
# Reglas: declaración con var, expresiones aritméticas, if-else,
# arreglos, función con retorno, reasignación y llamada a funciones
# Reglas semánticas de Pablo:
#   1) Una variable debe declararse antes de usarse
#   2) Una constante (let) no puede cambiar su valor

# Precedencia de operadores aritméticos (de menor a mayor)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'),    # menos unario: -x (Tabla 9, nivel 2)
)


# Regla semántica 1: devuelve el tipo de la variable si ya fue declarada.
# Si no fue declarada, guarda el error y devuelve None (tipo desconocido).
def buscar_variable(nombre, linea):
    if nombre not in tabla_simbolos['variables']:
        errores_semanticos.append(
            f"Error semántico en la línea {linea}: la variable '{nombre}' "
            f"se usa antes de declararse. Declárala antes con var o let, "
            f"por ejemplo: var {nombre} = 0.")
        return None
    tipo = tabla_simbolos['variables'][nombre]
    # Una variable ya no es un número literal: var x = 5 guarda Int (regla 5)
    return str(tipo) if tipo is not None else None


# Sentencias del aporte de Pablo
def p_sentencia_pablo(p):
    '''sentencia : declaracion
                 | if_else
                 | funcion
                 | retorno
                 | reasignacion
                 | llamada
                 | acceso'''


# Declaración de variable: var total = 5 + 3
def p_declaracion(p):
    'declaracion : VAR ID ASSIGN condicion'
    # Semántico: se guarda la variable con el tipo de su valor
    tabla_simbolos['variables'][p[2]] = p[4]


# Reasignación de una variable ya declarada: total = total + 5, contador += 1
def p_reasignacion(p):
    'reasignacion : destino operador_asig condicion'
    # La regla 2 se revisa en p_destino


# Lo que puede ir a la izquierda: una variable o un elemento del arreglo
def p_destino(p):
    '''destino : ID
               | ID LBRACKET expresion RBRACKET'''
    # Regla semántica 1: la variable debe estar declarada
    buscar_variable(p[1], p.lineno(1))
    # Regla semántica 2: una constante (let) no puede cambiar su valor
    if p[1] in tabla_simbolos['constantes']:
        if len(p) == 2:
            mensaje = (f"'{p[1]}' es una constante (let) y no se puede cambiar "
                       f"su valor. Si necesitas modificarla, declárala con var "
                       f"en lugar de let.")
        else:
            mensaje = (f"'{p[1]}' es un arreglo constante (let): no se pueden "
                       f"cambiar sus elementos. Si necesitas modificarlos, "
                       f"declara el arreglo con var.")
        errores_semanticos.append(
            f"Error semántico en la línea {p.lineno(1)}: {mensaje}")


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
# También sin parámetros: func obtenerTotal() -> Int { ... }
def p_funcion(p):
    '''funcion : FUNC ID LPAREN parametros RPAREN ARROW tipo LBRACE programa RBRACE
               | FUNC ID LPAREN RPAREN ARROW tipo LBRACE programa RBRACE'''
    # Sin parámetros la regla tiene un símbolo menos, así que el tipo
    # está en p[6] en lugar de p[7]
    if len(p) == 11:
        tipo = p[7]
    else:
        tipo = p[6]
    # Semántico (reglas de Jack): se guarda el tipo de retorno de la función
    # y se revisan los return que quedaron dentro de su cuerpo
    tabla_simbolos['funciones'][p[2]] = tipo
    revisar_retornos(p[2], tipo, p.lexpos(1), p.lexpos(len(p) - 1))


# Lista de parámetros separados por comas
def p_parametros(p):
    '''parametros : parametro
                  | parametros COMMA parametro'''


# Parámetro con su tipo: a: Int
def p_parametro(p):
    'parametro : ID COLON tipo'
    # Semántico: el parámetro queda declarado para usarlo en la función
    tabla_simbolos['variables'][p[1]] = p[3]


# Tipo de dato: Int, Double o arreglo como [Double]
def p_tipo(p):
    '''tipo : ID
            | LBRACKET ID RBRACKET'''
    # Semántico: devuelve el tipo, por ejemplo Int o [Double]
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"[{p[2]}]"


# Sentencia return con su valor
def p_retorno(p):
    'retorno : RETURN expresion'
    # Regla semántica 6 (Jack): se guarda hasta saber en qué función está
    registrar_retorno(p[2], p.lineno(1), p.lexpos(1))


# Condición simple: compara dos expresiones
def p_condicion(p):
    'condicion : expresion comparador expresion'
    # Semántico: una comparación da un valor de tipo Bool
    p[0] = 'Bool'


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
                 | MINUS expresion %prec UMINUS
                 | valor'''
    # Semántico: devuelve el tipo de la expresión
    if len(p) == 2:
        p[0] = p[1]                 # valor
    elif p[1] == '(':
        p[0] = p[2]                 # (expresion)
    elif p[1] == '-':
        p[0] = p[2]                 # -expresion: conserva el tipo
    else:
        # Regla semántica 5 (Jack): Int y Double no se mezclan sin convertir
        p[0] = revisar_conversion(p[1], p[3], p.lineno(2))


# Valores que pueden formar una expresión
def p_valor(p):
    '''valor : INT
             | DOUBLE
             | ID
             | arreglo
             | acceso
             | llamada'''
    # Semántico: devuelve el tipo del valor
    token = p.slice[1].type
    if token == 'INT':
        p[0] = TipoLiteral('Int')   # número escrito directamente (regla 5)
    elif token == 'DOUBLE':
        p[0] = 'Double'
    elif token == 'ID':
        # Regla semántica 1: la variable debe estar declarada
        p[0] = buscar_variable(p[1], p.lineno(1))
    else:
        p[0] = p[1]                 # arreglo, acceso o llamada


# Arreglo: [8.5, 9.0, 6.5]
def p_arreglo(p):
    'arreglo : LBRACKET elementos RBRACKET'
    # Semántico: el tipo se toma del primer elemento, por ejemplo [Double]
    p[0] = f"[{p[2]}]" if p[2] else None


# Elementos del arreglo separados por comas
def p_elementos(p):
    '''elementos : expresion
                 | elementos COMMA expresion'''
    # Semántico: se conserva el tipo del primer elemento
    p[0] = p[1]


# Acceso a un elemento del arreglo: notas[0]
def p_acceso(p):
    'acceso : ID LBRACKET expresion RBRACKET'
    # Regla semántica 1: el arreglo debe estar declarado
    tipo = buscar_variable(p[1], p.lineno(1))
    # Semántico: en un arreglo [Double] cada elemento es Double
    if tipo and tipo.startswith('[') and ':' not in tipo:
        p[0] = tipo[1:-1]
    else:
        p[0] = None


# Llamada a una función: sumar(a: 1, b: 2), saludar()
def p_llamada(p):
    '''llamada : ID LPAREN RPAREN
               | ID LPAREN argumentos RPAREN'''
    # Semántico (regla 5 de Jack): Double(x) da Double, Int(x) da Int y una
    # función ya declarada da su tipo de retorno
    p[0] = tipo_de_llamada(p[1])


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
# El valor puede ser una expresión o una condición: var activo: Bool = edad >= 18
def p_declaracion_tipada(p):
    'declaracion_tipada : VAR ID COLON tipo ASSIGN condicion'
    # Regla semántica 3: el valor debe coincidir con el tipo declarado
    nombre = p[2]
    tipo_declarado = p[4]
    tipo_valor = p[6]
    if not tipos_compatibles(tipo_declarado, tipo_valor):
        errores_semanticos.append(
            f"Error semántico en la línea {p.lineno(1)}: la variable "
            f"'{nombre}' es de tipo {tipo_declarado}, pero se le asigna un "
            f"valor de tipo {tipo_valor}. Asigna un valor de tipo "
            f"{tipo_declarado} o cambia el tipo de la variable.")
    # La variable se guarda con el tipo declarado
    tabla_simbolos['variables'][nombre] = tipo_declarado
 
 
# Regla semántica 3: compara el tipo declarado con el tipo del valor
def tipos_compatibles(tipo_declarado, tipo_valor):
    # Si no se conoce el tipo del valor, no se puede validar
    if tipo_valor is None:
        return True
    # Un diccionario vacío [:] sirve para cualquier tipo de diccionario
    if tipo_valor == 'DiccionarioVacio':
        return tipo_declarado.startswith('[') and ':' in tipo_declarado
    # Un número entero también se acepta como Double: var x: Double = 5
    if tipo_declarado == 'Double' and tipo_valor == 'Int':
        return True
    return tipo_declarado == tipo_valor
 
 
# Tipo diccionario: [String: Int]
def p_tipo_diccionario(p):
    'tipo : LBRACKET ID COLON ID RBRACKET'
    # Semántico: devuelve el tipo, por ejemplo [String: Int]
    p[0] = f"[{p[2]}: {p[4]}]"
 
 
# Estructura de control while: while contador < 10 { contador += 1 }
def p_ciclo_while(p):
    'ciclo_while : WHILE condicion LBRACE programa RBRACE'
    # Regla semántica 4: los break/continue de este while son válidos
    cerrar_ciclo(p.lexpos(1), p.lexpos(5))
 
 
# Regla semántica 4: break y continue encontrados que aún no están
# dentro de un ciclo. Cada uno se guarda con su línea y su posición.
controles_pendientes = []
 
 
# Al cerrar un ciclo se quitan los break/continue que están entre
# la palabra while o for y la llave que cierra el ciclo
def cerrar_ciclo(inicio, fin):
    for control in controles_pendientes[:]:
        if inicio < control['posicion'] < fin:
            controles_pendientes.remove(control)
 
 
# Al terminar el análisis, los que quedaron pendientes están fuera de un ciclo
def verificar_control_ciclo():
    for control in controles_pendientes:
        errores_semanticos.append(
            f"Error semántico en la línea {control['linea']}: "
            f"'{control['palabra']}' solo puede usarse dentro de un ciclo "
            f"while o for. Muévelo dentro de un ciclo o elimínalo.")
 
 
# Control del ciclo: break y continue
def p_control_ciclo(p):
    '''control_ciclo : BREAK
                     | CONTINUE'''
    # Regla semántica 4: se guarda hasta saber si está dentro de un ciclo
    controles_pendientes.append({'palabra': p[1],
                                 'linea': p.lineno(1),
                                 'posicion': p.lexpos(1)})
 
 
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
    # Semántico: una cadena es de tipo String
    if isinstance(p[1], str) and p.slice[1].type == 'STRING':
        p[0] = 'String'
    else:
        p[0] = p[1]
 
 
# Diccionario con pares clave: valor, o vacío: ["Danna": 21, "Pablo": 17], [:]
def p_diccionario(p):
    '''diccionario : LBRACKET pares RBRACKET
                   | LBRACKET COLON RBRACKET'''
    # Semántico: el tipo se toma del primer par, por ejemplo [String: Int]
    if p[2] == ':':
        p[0] = 'DiccionarioVacio'
    elif p[2][0] is None or p[2][1] is None:
        p[0] = None
    else:
        p[0] = f"[{p[2][0]}: {p[2][1]}]"
 
 
# Pares clave: valor separados por comas
def p_pares(p):
    '''pares : par
             | pares COMMA par'''
    # Semántico: se conservan los tipos del primer par
    p[0] = p[1]
 
 
# Par clave: valor
def p_par(p):
    'par : expresion COLON expresion'
    # Semántico: devuelve el tipo de la clave y el tipo del valor
    p[0] = (p[1], p[3])
 
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
    # Semántico: la constante se guarda con su tipo y se marca como let
    tabla_simbolos['variables'][p[2]] = p[4]
    tabla_simbolos['constantes'].add(p[2])


# Declaración de una constante indicando su tipo: let nombre: String = "Jack"
def p_declaracion_constante_tipada(p):
    'declaracion_constante_tipada : LET ID COLON tipo ASSIGN expresion'
    # Semántico: la constante se guarda con su tipo y se marca como let
    tabla_simbolos['variables'][p[2]] = p[4]
    tabla_simbolos['constantes'].add(p[2])


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
    # Semántico: la condición tiene el mismo tipo que la expresión
    p[0] = p[1]


# Ciclo for-in para recorrer una lista: for numero in numeros { ... }
def p_ciclo_for(p):
    'ciclo_for : FOR variable_for IN expresion LBRACE programa RBRACE'
    # Semántico: los break/continue de este for son válidos
    cerrar_ciclo(p.lexpos(1), p.lexpos(7))


# Variable del for: se declara antes de analizar el cuerpo del ciclo
def p_variable_for(p):
    'variable_for : ID'
    tabla_simbolos['variables'][p[1]] = None


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
    # Semántico: true y false son Bool; nil, tuplas y readLine() no se validan
    if p.slice[1].type in ('TRUE', 'FALSE'):
        p[0] = 'Bool'
    else:
        p[0] = None


# Tupla de dos o más valores, que pueden ser de distinto tipo: (3, 4), ("Ana", 20)
def p_tupla(p):
    'tupla : LPAREN expresion COMMA elementos RPAREN'


# Lectura de un dato ingresado por teclado: readLine()
def p_lectura(p):
    'lectura : READLINE LPAREN RPAREN'


# ----- Reglas semánticas de Jack Vera -----
# Regla 5: para operar un Int con un Double se debe convertir uno de ellos
# Regla 6: el valor de return debe coincidir con el tipo de retorno

# Tipo de un número entero escrito directamente, como 5 o 10. Se compara
# igual que 'Int', pero Swift lo adapta a Double si se opera con un Double:
# precio * 2 es válido, pero cantidad * precio no.
class TipoLiteral(str):
    pass


# Regla semántica 5: revisa una operación aritmética y devuelve su tipo
def revisar_conversion(izquierda, derecha, linea):
    # Si no se conoce el tipo de uno de los lados, no se puede validar
    if izquierda is None or derecha is None:
        return None
    if izquierda == derecha:
        # Solo sigue siendo literal si los dos lados lo son: 2 + 3
        if isinstance(izquierda, TipoLiteral) and isinstance(derecha, TipoLiteral):
            return izquierda
        return str(izquierda)
    if {izquierda, derecha} == {'Int', 'Double'}:
        # Un número entero escrito directamente se adapta a Double
        if isinstance(izquierda, TipoLiteral) or isinstance(derecha, TipoLiteral):
            return 'Double'
        errores_semanticos.append(
            f"Error semántico en la línea {linea}: no se puede operar un Int "
            f"con un Double sin convertirlos. Convierte uno de los dos, por "
            f"ejemplo: Double(entero) o Int(decimal).")
    return None


# Regla semántica 5: Double(x) e Int(x) son conversiones explícitas.
# Una función ya declarada devuelve su tipo de retorno.
def tipo_de_llamada(nombre):
    if nombre in ('Int', 'Double', 'String'):
        return nombre
    return tabla_simbolos['funciones'].get(nombre)


# Regla semántica 6: return encontrados que aún no se revisan. Cada uno se
# guarda con su tipo, su línea y su posición, igual que break y continue.
retornos_pendientes = []


def registrar_retorno(tipo, linea, posicion):
    retornos_pendientes.append({'tipo': tipo, 'linea': linea,
                                'posicion': posicion})


# Al cerrar una función con retorno se revisan los return que están entre
# la palabra func y la llave que cierra la función
def revisar_retornos(nombre, tipo_funcion, inicio, fin):
    for retorno in retornos_pendientes[:]:
        if inicio < retorno['posicion'] < fin:
            retornos_pendientes.remove(retorno)
            if not retorno_compatible(tipo_funcion, retorno['tipo']):
                errores_semanticos.append(
                    f"Error semántico en la línea {retorno['linea']}: la "
                    f"función '{nombre}' debe devolver {tipo_funcion}, pero el "
                    f"return devuelve {retorno['tipo']}. Devuelve un valor de "
                    f"tipo {tipo_funcion} o cambia el tipo de retorno de la "
                    f"función.")


def retorno_compatible(tipo_funcion, tipo_valor):
    # Si no se conoce el tipo del valor, no se puede validar
    if tipo_valor is None:
        return True
    # Un número entero escrito directamente sirve para una función Double
    if tipo_funcion == 'Double' and isinstance(tipo_valor, TipoLiteral):
        return True
    return tipo_funcion == tipo_valor

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


# Limpia el estado global y analiza el código una vez.
# Un solo recorrido del parser llena los errores sintácticos y los semánticos.
def _parsear(codigo):
    errores.clear()
    errores_semanticos.clear()
    tabla_simbolos['variables'].clear()
    tabla_simbolos['constantes'].clear()
    controles_pendientes.clear()
    tabla_simbolos['funciones'].clear()
    retornos_pendientes.clear()
    analizador_lexico.lexer.lineno = 1
    parser.parse(codigo, lexer=analizador_lexico.lexer)
    verificar_control_ciclo()


# Escribe un log en logs/ y devuelve su nombre
def _escribir_log(prefijo, titulo, encabezado, sin_errores, lista,
                  usuario, ruta_algoritmo, ahora):
    nombre_log = (f"{prefijo}-{usuario}-"
                  f"{ahora.strftime('%d%m%Y')}-{ahora.strftime('%Hh%M')}.txt")
    os.makedirs('logs', exist_ok=True)
    ruta_log = os.path.join('logs', nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write(f"{titulo} - SwiftLearn\n")
        log.write(f"Archivo: {ruta_algoritmo}\n")
        log.write(f"Desarrollador: {usuario}\n")
        log.write(f"Fecha: {ahora.strftime('%d-%m-%Y %H:%M')}\n\n")
        log.write(f"{encabezado} ({len(lista)})\n")
        log.write("\n".join(lista) if lista else sin_errores)
        log.write("\n")
    return nombre_log


def analizar_sintactico(codigo, usuario, ruta_algoritmo='(editor)', ahora=None):
    """Análisis sintáctico de un texto. Genera solo el log sintáctico.

    Devuelve {'errores': [...], 'log': nombre_del_log}.
    """
    _parsear(codigo)
    ahora = ahora or datetime.now()
    nombre_log = _escribir_log('sintactico', 'ANÁLISIS SINTÁCTICO',
                               'ERRORES SINTÁCTICOS',
                               'Sin errores sintácticos.', errores,
                               usuario, ruta_algoritmo, ahora)
    return {'errores': list(errores), 'log': nombre_log}


def analizar_semantico(codigo, usuario, ruta_algoritmo='(editor)', ahora=None):
    """Análisis semántico de un texto. Genera solo el log semántico.

    Devuelve {'errores': [...], 'errores_sintacticos': N, 'log': nombre}.
    'errores_sintacticos' sirve para avisar que hay que corregirlos primero.
    """
    _parsear(codigo)
    ahora = ahora or datetime.now()
    nombre_log = _escribir_log('semantico', 'ANÁLISIS SEMÁNTICO',
                               'ERRORES SEMÁNTICOS',
                               'Sin errores semánticos.', errores_semanticos,
                               usuario, ruta_algoritmo, ahora)
    return {'errores': list(errores_semanticos),
            'errores_sintacticos': len(errores),
            'log': nombre_log}


def analizar(ruta_algoritmo, usuario):
    """Analiza un archivo Swift desde la consola y genera los dos logs."""
    with open(ruta_algoritmo, encoding='utf-8') as archivo:
        codigo = archivo.read()

    # Una sola fecha para que los dos logs tengan la misma hora
    ahora = datetime.now()

    sintactico = analizar_sintactico(codigo, usuario, ruta_algoritmo, ahora)
    print(f"Errores sintácticos: {len(sintactico['errores'])}")
    for error in sintactico['errores']:
        print(f"  {error}")
    print(f"Log generado: {os.path.join('logs', sintactico['log'])}")

    semantico = analizar_semantico(codigo, usuario, ruta_algoritmo, ahora)
    print(f"Errores semánticos: {len(semantico['errores'])}")
    for error in semantico['errores']:
        print(f"  {error}")
    print(f"Log generado: {os.path.join('logs', semantico['log'])}")



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python parser.py <ruta_algoritmo.swift> <usuarioGit>")
        sys.exit(1)
    analizar(sys.argv[1], sys.argv[2])
