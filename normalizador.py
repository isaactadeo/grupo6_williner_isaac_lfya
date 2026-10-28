import ast
import copy

class NormalizadorAST(ast.NodeTransformer):
    def __init__(self):
        self.variables_vistas = {}
        self.contador_var = 1

    def obtener_nombre_var(self, nombre_original):
        if nombre_original not in self.variables_vistas:
            self.variables_vistas[nombre_original] = f"VAR{self.contador_var}"
            self.contador_var += 1
        return self.variables_vistas[nombre_original]

    def visit_Name(self, nodo):
        nodo.id = self.obtener_nombre_var(nodo.id)
        return self.generic_visit(nodo)

    def visit_arg(self, nodo):
        nodo.arg = self.obtener_nombre_var(nodo.arg)
        return self.generic_visit(nodo)

    def visit_Constant(self, nodo):
        nodo.value = "LIT"
        return self.generic_visit(nodo)
    
    def visit_FunctionDef(self, nodo):
        nodo.name = "FUNC"
        return self.generic_visit(nodo)

    def visit_AsyncFunctionDef(self, nodo):
        nodo.name = "FUNC_ASYNC"
        return self.generic_visit(nodo)

def normalizar_funcion(nodo_ast):
    nodo_copia = copy.deepcopy(nodo_ast)
    normalizador = NormalizadorAST()
    return normalizador.visit(nodo_copia)