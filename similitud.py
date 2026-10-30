import ast

class SerializadorAST(ast.NodeVisitor):
    def __init__(self):
        self.tokens = []

    def generic_visit(self, nodo):
        token = type(nodo).__name__
        
        if hasattr(nodo, 'id'):
            token += f":{nodo.id}"
        elif hasattr(nodo, 'arg'):
            token += f":{nodo.arg}"
        elif hasattr(nodo, 'value') and isinstance(nodo.value, str) and nodo.value == "LIT":
             token += f":{nodo.value}"
        elif hasattr(nodo, 'name'):
            token += f":{nodo.name}"

        self.tokens.append(token)
        super().generic_visit(nodo) 

def obtener_secuencia_tokens(nodo_normalizado):
    serializador = SerializadorAST()
    serializador.visit(nodo_normalizado)
    return serializador.tokens

def extraer_ngramas(secuencia, n=3):
    return [tuple(secuencia[i:i+n]) for i in range(len(secuencia) - n + 1)]

def calcular_similitud_jaccard(tokens1, tokens2, n=3):
    ngramas1 = set(extraer_ngramas(tokens1, n))
    ngramas2 = set(extraer_ngramas(tokens2, n))
    
    if not ngramas1 and not ngramas2:
        return 1.0
    if not ngramas1 or not ngramas2:
        return 0.0
        
    interseccion = len(ngramas1.intersection(ngramas2))
    union = len(ngramas1.union(ngramas2))
    
    return interseccion / union

UMBRAL_DUPLICADO = 0.8