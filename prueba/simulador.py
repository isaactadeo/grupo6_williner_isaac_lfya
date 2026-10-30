def calcular_total(precios):
    suma = 0
    for p in precios:
        suma += p
    return suma

def sacar_suma_final(valores_crudos):
    acumulador = 0
    for v in valores_crudos:
        acumulador += v
    return acumulador

def imprimir_mensaje(texto):
    print("El mensaje es: " + texto)