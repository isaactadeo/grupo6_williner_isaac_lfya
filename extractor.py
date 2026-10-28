import ast
import os

class ExploradorDeFunciones(ast.NodeVisitor):
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.funciones_encontradas = []

    def visit_FunctionDef(self, nodo):
        self.funciones_encontradas.append({
            'nombre': nodo.name,
            'archivo': self.ruta_archivo,
            'linea': nodo.lineno,
            'nodo_ast': nodo
        })
        self.generic_visit(nodo)

    def visit_AsyncFunctionDef(self, nodo):
        self.visit_FunctionDef(nodo)

def recolectar_funciones(carpeta_objetivo):
    todas_las_funciones = []
    for raiz, _, archivos in os.walk(carpeta_objetivo):
        for archivo in archivos:
            if archivo.endswith('.py'):
                ruta_completa = os.path.join(raiz, archivo)
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        arbol = ast.parse(f.read(), filename=ruta_completa)
                        explorador = ExploradorDeFunciones(ruta_completa)
                        explorador.visit(arbol)
                        todas_las_funciones.extend(explorador.funciones_encontradas)
                except Exception:
                    pass
    return todas_las_funciones