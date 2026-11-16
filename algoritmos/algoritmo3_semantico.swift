// Algoritmo 3 (semántico) - Jack Vera
// Valida las reglas semánticas del aporte de Jack:
// 5. Para operar un Int con un Double se debe convertir uno de ellos
// 6. El valor de return debe coincidir con el tipo de retorno de la función

/* Regla 5: operaciones válidas entre Int y Double */
let cantidad = 3
let precio = 2.5
var total = Double(cantidad) * precio
var entero = cantidad + Int(precio)
var doble = precio * 2
var mitad = (precio + 7.5) / 2
var residuo = 10 % 4

/* Regla 6: cada función devuelve un valor de su tipo de retorno */
func sumar(a: Int, b: Int) -> Int {
    return a + b
}

func promediar(suma: Double, n: Int) -> Double {
    return suma / Double(n)
}

func esPar(numero: Int) -> Bool {
    if numero % 2 == 0 {
        return true
    } else {
        return false
    }
}

func escalar(valor: Double) -> Double {
    return valor * 2
}

var resultado = sumar(a: cantidad, b: 4) + 1
var promedio = promediar(suma: total, n: cantidad) * 1.5

/* La variable del for también se puede usar dentro del ciclo */
let notas = [7.5, 8.0, 9.5]
var acumulado = 0.0
for nota in notas {
    acumulado += nota
}

// ===== Errores semánticos intencionales para la prueba =====

// Error 1: se suma un Int con un Double sin convertir
var mezcla = cantidad + precio

// Error 2: se multiplica una variable Int por un número decimal
var descuento = cantidad * 0.5

// Error 3: se divide un Double entre el Int que devuelve una función
var division = precio / sumar(a: 1, b: 2)

// Error 4: la función debe devolver Int, pero devuelve un Double
func redondear(valor: Double) -> Int {
    return valor
}

// Error 5: la función debe devolver Double, pero devuelve un Int sin convertir
func convertir(numero: Int) -> Double {
    return numero
}

// Error 6: la función debe devolver Bool, pero devuelve un String
func aprobado(calificacion: Double) -> Bool {
    return "si"
}
