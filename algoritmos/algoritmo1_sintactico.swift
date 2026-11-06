// Algoritmo 1 (sintáctico) - Pablo Chacón
// Valida las reglas sintácticas del aporte de Pablo:
// declaración con var, expresiones aritméticas, if-else,
// arreglos, función con retorno, reasignación y llamada a funciones

/* Arreglo y acceso a sus elementos */
var notas = [8.5, 9.0, 6.5, 10.0]
var primera = notas[0]
var ultima = notas[3]

/* Expresiones aritméticas con uno o más operadores */
var cantidad = 4
var suma = notas[0] + notas[1] + notas[2] + notas[3]
var promedio = suma / 4.0
var ajuste = (primera + ultima) * 2 - 1
var residuo = cantidad % 3

/* Función con retorno, con varios parámetros y un arreglo */
func calcularPromedio(lista: [Double], total: Double) -> Double {
    var resultado = (lista[0] + lista[1]) / total
    return resultado
}

/* Función con retorno que usa if-else dentro */
func mayorQue(a: Int, b: Int) -> Int {
    if a > b {
        return a
    } else {
        return b
    }
}

/* if-else con varias instrucciones en cada bloque */
if promedio >= 7.0 {
    var aprobado = 1
    var bono = promedio * 0.1
} else {
    var aprobado = 0
    var bono = 0
}

/* Llamadas a funciones, con y sin etiqueta */
var promedioFinal = calcularPromedio(lista: notas, total: 2.0)
var mayor = mayorQue(a: 7, b: cantidad) * 2
var decimal = Double(cantidad)

/* Reasignación con = y con operadores compuestos */
suma = suma + 1
notas[0] = 9.5
cantidad += 1
cantidad -= 2
ajuste *= 3
ajuste /= 2
residuo %= 2

/* if sin else */
if residuo == 0 {
    var exacto = 1
}

// ===== Errores sintácticos intencionales para la prueba =====

// Error 1: falta el nombre de la variable
var = 10

// Error 2: arreglo con una coma de más al final
var pares = [2, 4, 6,]

// Error 3: else sin llaves
if cantidad > 2 {
    var mayor = 1
} else
var menor = 0
