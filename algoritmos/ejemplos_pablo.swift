// ===== Ejemplos para la sustentación: Pablo Chacón =====
// Todo este archivo da 0 errores en los 3 análisis.
// Para la sustentación: copia solo el bloque que pida el profe.

// ---------- 1. Estructura de control: if-else ----------

// 1a. if con else
var edad = 20
if edad >= 18 {
    print("Mayor de edad")
} else {
    print("Menor de edad")
}

// 1b. if sin else
var nota = 8.5
if nota >= 7.0 {
    print("Aprobado")
}

// 1c. if dentro de otro if
var temperatura = 30
if temperatura > 25 {
    if temperatura > 35 {
        print("Muy caluroso")
    } else {
        print("Caluroso")
    }
} else {
    print("Fresco")
}

// ---------- 2. Estructura de datos: arreglos ----------

// 2a. declarar, acceder y modificar
var notas = [8, 9, 10]
var primera = notas[0]
notas[1] = 7

// 2b. arreglos de distintos tipos
var precios = [2.5, 3.75, 10.0]
var nombres = ["Ana", "Luis", "Pedro"]
var matriz = [[1, 2], [3, 4]]

// 2c. índice calculado con una expresión
var edades = [18, 25, 40]
var indice = 1
var ultima = edades[indice + 1]

// ---------- 3. Tipo de función: función con retorno ----------

// 3a. con parámetros, y su llamada
func sumar(a: Int, b: Int) -> Int {
    return a + b
}
var resultado = sumar(a: 3, b: 4)

// 3b. devuelve un Double
func promedio(n1: Double, n2: Double, n3: Double) -> Double {
    return (n1 + n2 + n3) / 3.0
}
var miPromedio = promedio(n1: 8.0, n2: 9.0, n3: 10.0)

// 3c. sin parámetros
func obtenerMaximo() -> Int {
    return 100
}
var maximo = obtenerMaximo()

// ---------- 4. Expresiones aritméticas ----------
var x = 10
var y = -x
var z = (x + 2) * 3 % 4
x += 5

// ---------- 5. Regla semántica 1: declarar antes de usar ----------
var total = 0
total = total + 5
print(total)

// ---------- 6. Regla semántica 2: una constante (let) no cambia ----------
let pi = 3.14
var area = pi * 2.0 * 2.0
let dias = [1, 2, 3]
var primerDia = dias[0]
