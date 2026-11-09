// Algoritmo 3 (sintáctico) - Jack Vera
// Prueba las reglas sintácticas de mi aporte: constantes con let,
// expresiones booleanas, ciclo for-in, tuplas, función sin parámetros,
// lectura con readLine, los valores true, false y nil, y el punto y coma

/* Constantes con let, con y sin tipo */
let pi = 3.14
let nombre: String = "Jack"
let numeros = [2, 4, 6, 8, 10]
let limite: Int = 10;

/* Valores nuevos: true, false, nil, tuplas y readLine */
var activo = true
var bloqueado = false
var apodo = nil
let punto = (3, 4)
let persona = ("Ana", 20, true)
var entrada = readLine()
var edad = 18;

/* Función sin parámetros */
func mostrar() {
    print("Hola,", nombre);
    print("Punto:", punto)
}

mostrar()

/* Ciclo for-in que suma los números pares de la lista */
var suma = 0
for numero in numeros {
    if numero % 2 == 0 {
        suma += numero;
    }
}

/* Expresiones booleanas con &&, || y ! */
if edad >= 18 && activo || !bloqueado {
    print("Acceso permitido")
} else {
    print("Acceso denegado")
}

// Una sola variable como condición
if activo {
    print("Usuario activo")
}

while !bloqueado && suma > limite {
    suma -= 1
}

// Condición con paréntesis y dos instrucciones en la misma línea separadas por ;
if suma > limite || (edad >= 18 && !bloqueado) {
    print("La suma es", suma); print("Fin")
}

// ===== Errores sintácticos a propósito para la prueba =====

// Error 1: falta el nombre de la constante después de let
let = 5
suma = 0

// Error 2: falta la segunda condición después de &&
if activo && {
}
suma = 0

// Error 3: al for le falta la palabra in
for numero numeros {
}
suma = 0

// Error 4: a la función le faltan los paréntesis
func mostrarTodo {
}
suma = 0