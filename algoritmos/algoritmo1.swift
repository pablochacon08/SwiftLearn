// Algoritmo 1 - Pablo Chacón
// Calcula el promedio de las notas de un estudiante e indica si aprobó

/* Declaración de variables, constante y arreglo */
var notas: [Double] = [8.5, 9.0, 6.5, 10.0]
var cantidad = 4
let notaMinima = 7.0

// Función con retorno: suma los elementos del arreglo
func sumar(lista: [Double], n: Int) -> Double {
    var total = 0.0
    var i = 0
    while i < n {
        total = total + lista[i]
        i += 1
    }
    return total
}

// Función con retorno: calcula el promedio
func calcularPromedio(suma: Double, n: Int) -> Double {
    return suma / Double(n)
}

var suma = sumar(lista: notas, n: cantidad)
var promedio = calcularPromedio(suma: suma, n: cantidad)

// Estructura de control if-else
if promedio >= notaMinima && cantidad > 0 {
    print("Aprobado con promedio:", promedio)
} else {
    print("Reprobado con promedio:", promedio)
}

// Operadores aritméticos y acceso al arreglo
var puntosExtra = 15 % 4 * 2 - 1
notas[0] = notas[0] + 0.5
print("Puntos extra:", puntosExtra)

// Error léxico intencional para la prueba
var bono = 5¿