// Algoritmo 1 (semántico) - Pablo Chacón
// Valida las reglas semánticas del aporte de Pablo:
// 1. Una variable debe declararse antes de usarse
// 2. Una constante (let) no puede cambiar su valor

/* Regla 1: variables declaradas antes de usarse */
var notas = [8.5, 9.0, 6.5, 10.0]
var cantidad = 4
var suma = notas[0] + notas[1] + notas[2] + notas[3]
var promedio = suma / 4.0
var residuo = cantidad % 3

/* Regla 1: los parámetros quedan declarados dentro de la función */
func calcularPromedio(lista: [Double], total: Double) -> Double {
    var resultado = (lista[0] + lista[1]) / total
    return resultado
}

func mayorQue(a: Int, b: Int) -> Int {
    if a > b {
        return a
    } else {
        return b
    }
}

var promedioFinal = calcularPromedio(lista: notas, total: 2.0)
var mayor = mayorQue(a: 7, b: cantidad) * 2

/* Regla 2: una variable (var) sí puede cambiar su valor */
suma = suma + 1.0
notas[0] = 9.5
cantidad += 1
cantidad -= 2
cantidad *= 3
promedio /= 2.0
residuo %= 2

/* Regla 2: una constante (let) se puede leer, pero no cambiar */
let maximo = 10
let pesos = [0.3, 0.7]
var limite = maximo - 1
var primerPeso = pesos[0] * 2.0

// ===== Errores semánticos intencionales para la prueba =====

// Error 1: se usa una variable que nunca se declaró
var total = cantidad + bono

// Error 2: se reasigna una variable que no fue declarada
contador = 5

// Error 3: se accede a un arreglo que no fue declarado
var dato = valores[1]

// Error 4: se usa la variable antes de su declaración
var doble = triple * 2
var triple = 3

// Error 5: se cambia el valor de una constante
maximo = 20

// Error 6: se cambia una constante con un operador compuesto
maximo += 5

// Error 7: se cambia un elemento de un arreglo constante
pesos[1] = 0.5
