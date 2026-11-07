// Algoritmo 2 (sintáctico) - Danna Ayala
// Valida las reglas sintácticas del aporte de Danna:
// declaración con anotación de tipo, while con break y continue,
// diccionarios, función sin retorno con parámetros e impresión

/* Declaración con anotación de tipo */
var nombre: String = "Danna"
var contador: Int = 0
var limite: Int = 10
var promedio: Double = 8.5 * 2 - 1

/* Diccionario: declaración, vacío, acceso y modificación */
var edades: [String: Int] = ["Danna": 21, "Pablo": 17, "Sofia": 22]
var notas = ["Danna": 9.5, "Pablo": 8.0]
var vacio: [String: Int] = [:]
var edadPablo: Int = edades["Pablo"]
edades["Pablo"] = 18
vacio["Jack"] = 20

/* Función sin retorno con parámetros */
func saludar(nombre: String, edad: Int) {
    print("Hola", nombre)
    print("Tienes", edad, "años")
}

saludar(nombre: nombre, edad: 21)

/* Ciclo while con break y continue */
while contador <= limite {
    contador += 1
    if contador % 2 == 0 {
        continue
    }
    if contador > 7 {
        break
    }
    print("Número impar:", contador)
}

/* Impresión de cadenas, variables, expresiones y diccionarios */
print("Fin del ciclo")
print(contador)
print("El doble es", contador * 2)
print(edades["Danna"])

// ===== Errores sintácticos intencionales para la prueba =====

// Error 1: falta el tipo después de los dos puntos
var apellido: = "Ayala"
contador = 0

// Error 2: par del diccionario sin dos puntos
var ciudades = ["Quito": 1, "Guayaquil" 2]
contador = 0

// Error 3: print sin paréntesis
print "Adiós"
contador = 0

// Error 4: while sin llaves
while contador < 20
contador += 1