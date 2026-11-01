// Algoritmo 2 - Danna Ayala
// Recorre números con un ciclo while y usa un diccionario de edades

/* El ciclo salta los números pares con continue
   y termina con break al pasar de 7 */

var nombre: String = "Danna"
var edades: [String: Int] = ["Danna": 21, "Pablo": 17, "Sofia": 22]
var contador: Int = 0
var limite: Int = 10
var edadPablo: Int = 17

func saludar(nombre: String) {
    print("Hola", nombre)
}

saludar(nombre: nombre)

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

if edadPablo >= 18 {
    print("Pablo es mayor de edad")
} else {
    print("Pablo es menor de edad")
}

if nombre != "Pablo" && contador < limite {
    print("El ciclo terminó antes del límite")
}