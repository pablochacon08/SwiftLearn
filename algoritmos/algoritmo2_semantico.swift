// Algoritmo 2 (semántico) - Danna Ayala
// Valida las reglas semánticas del aporte de Danna:
// 1. El valor asignado debe coincidir con el tipo declarado
// 2. break y continue solo pueden usarse dentro de un ciclo

/* Regla 1: declaraciones válidas */
var nombre: String = "Danna"
var edad: Int = 21
var promedio: Double = 8.5
var bono: Double = 2
var total: Int = edad + 4
var saludo: String = "Hola " + nombre
var edades: [String: Int] = ["Danna": 21, "Pablo": 17]
var vacio: [String: Int] = [:]
var copiaEdad: Int = edad

/* Regla 2: break y continue dentro de ciclos */
var contador: Int = 0
while contador < 10 {
    contador += 1
    if contador % 2 == 0 {
        continue
    }
    if contador > 7 {
        break
    }
}

let numeros = [1, 2, 3, 4]
for numero in numeros {
    if numero == 3 {
        break
    }
}

// ===== Errores semánticos intencionales para la prueba =====

// Error 1: se asigna una cadena a una variable Int
var anios: Int = "veinte"

// Error 2: se asigna un número a una variable String
var apellido: String = 25

// Error 3: se asigna una variable Int a una variable String
var texto: String = edad

// Error 4: el diccionario tiene valores String, pero se declaró [String: Int]
var notas: [String: Int] = ["Danna": "alta", "Pablo": "media"]

// Error 5: break fuera de un ciclo
if edad > 18 {
    break
}

// Error 6: continue fuera de un ciclo
continue