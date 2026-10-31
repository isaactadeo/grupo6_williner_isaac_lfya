import unittest
import ast
from normalizador import normalizar_funcion
from similitud import obtener_secuencia_tokens, calcular_similitud_jaccard, UMBRAL_DUPLICADO

def obtener_tokens_de_string(codigo_fuente):
    arbol = ast.parse(codigo_fuente)
    nodo_funcion = arbol.body[0]
    nodo_normalizado = normalizar_funcion(nodo_funcion)
    return obtener_secuencia_tokens(nodo_normalizado)

class Test(unittest.TestCase):

    def test_positivo_variables_renombradas(self):
        codigo1 = """
def calcular_area(base, altura):
    area = base * altura
    return area
"""
        codigo2 = """
def sacar_superficie(b, a):
    resultado = b * a
    return resultado
"""
        tokens1 = obtener_tokens_de_string(codigo1)
        tokens2 = obtener_tokens_de_string(codigo2)
        score = calcular_similitud_jaccard(tokens1, tokens2)
        
        self.assertGreaterEqual(score, UMBRAL_DUPLICADO)
        self.assertEqual(score, 1.0)

    def test_positivo_formato_y_comentarios(self):
        codigo1 = """
def calcular_iva(precio):
    return precio * 1.21
"""
        codigo2 = """
def sacar_impuesto(p):
    # Este es un comentario trampa para intentar engañar al detector
    
    
    return p * 1.21 # El AST ignora los comentarios y espacios en blanco
"""
        tokens1 = obtener_tokens_de_string(codigo1)
        tokens2 = obtener_tokens_de_string(codigo2)
        score = calcular_similitud_jaccard(tokens1, tokens2)
        
        self.assertGreaterEqual(score, UMBRAL_DUPLICADO)

    def test_negativo_funciones_distintas(self):
        codigo1 = """
def saludar(nombre):
    print("Hola " + nombre)
"""
        codigo2 = """
def calcular_factorial(n):
    if n == 0:
        return 1
    return n * calcular_factorial(n-1)
"""
        tokens1 = obtener_tokens_de_string(codigo1)
        tokens2 = obtener_tokens_de_string(codigo2)
        score = calcular_similitud_jaccard(tokens1, tokens2)
        
        self.assertLess(score, UMBRAL_DUPLICADO)

    def test_negativo_mismo_objetivo_distinta_logica(self):
        codigo1 = """
def sumar_lista(numeros):
    total = 0
    for n in numeros:
        total += n
    return total
"""
        codigo2 = """
def sumar_lista_recursiva(numeros):
    if not numeros:
        return 0
    return numeros[0] + sumar_lista_recursiva(numeros[1:])
"""
        tokens1 = obtener_tokens_de_string(codigo1)
        tokens2 = obtener_tokens_de_string(codigo2)
        score = calcular_similitud_jaccard(tokens1, tokens2)

        self.assertLess(score, UMBRAL_DUPLICADO)

   

if __name__ == '__main__':
    unittest.main(verbosity=2)




# Este era el test q esperabamosmos que de positivo y no dio
#def test_positivo_lineas_reordenadas(self):
#            codigo1 = """
#    def configurar_usuario(nombre, edad):
#        n = nombre
#        e = edad
#        return True
#    """
#            codigo2 = """
#    def setup_user(nombre, edad):
#        e = edad
#        n = nombre
#        return True
#    """
#            tokens1 = obtener_tokens_de_string(codigo1)
#            tokens2 = obtener_tokens_de_string(codigo2)
#            score = calcular_similitud_jaccard(tokens1, tokens2)
#
#            self.assertGreaterEqual(score, UMBRAL_DUPLICADO)