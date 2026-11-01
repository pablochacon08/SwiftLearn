// Algoritmo 3 - Jack Vera
// Recorre una lista, suma los valores pares y muestra el resultado

// Declara una lista de numero y una variable para la suma
let numeros = [2, 4, 6, 8]
var suma = 0


// Recorre la lista con un ciclo y sima los numeros que son pares, y la guarda en la variable suma
for numero in numeros {
    if numero % 2 == 0 {
        suma += numero;
    }
}

// Flujo de control para mostrar si la suma es mayor que diez o no
if suma > 10 {
    print("La suma es mayor que diez:", suma)
} else {
    print("La suma no es mayor que diez:", suma)
}

// Declara la variable resultado con el valor de la suma y una contante sin valor, luego se imprime el resultado
var resultado: Int = suma
let sinValor = nil
print("Resultado:", resultado)
