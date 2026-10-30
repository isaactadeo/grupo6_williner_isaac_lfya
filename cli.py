import argparse
from extractor import recolectar_funciones
from normalizador import normalizar_funcion
from similitud import obtener_secuencia_tokens, calcular_similitud_jaccard

def iniciar_buscador():
    parser = argparse.ArgumentParser(description="Buscador de clones de código AST")
    parser.add_argument('--dir', required=True, help="Carpeta local con los archivos .py")
    parser.add_argument('--funcion', required=True, help="Formato esperado: archivo.py:nombre_funcion")
    parser.add_argument('--top', type=int, default=5, help="Cantidad de resultados a mostrar")
    
    args = parser.parse_args()

    todas_las_funciones = recolectar_funciones(args.dir)
    
    try:
        objetivo_archivo, objetivo_nombre = args.funcion.split(':')
    except ValueError:
        print("Error: El argumento --funcion debe tener el formato archivo.py:nombre_funcion")
        return

    funcion_objetivo = None
    for f in todas_las_funciones:
        if f['archivo'].endswith(objetivo_archivo) and f['nombre'] == objetivo_nombre:
            funcion_objetivo = f
            break

    if not funcion_objetivo:
        print(f"No se encontró la función {objetivo_nombre} en {objetivo_archivo}.")
        return

    nodo_obj_normalizado = normalizar_funcion(funcion_objetivo['nodo_ast'])
    tokens_objetivo = obtener_secuencia_tokens(nodo_obj_normalizado)

    resultados = []
    for f in todas_las_funciones:
        if f['archivo'] == funcion_objetivo['archivo'] and f['nombre'] == funcion_objetivo['nombre']:
            continue
            
        nodo_normalizado = normalizar_funcion(f['nodo_ast'])
        tokens_candidato = obtener_secuencia_tokens(nodo_normalizado)
        
        score = calcular_similitud_jaccard(tokens_objetivo, tokens_candidato)
        
        resultados.append({
            'archivo': f['archivo'],
            'nombre': f['nombre'],
            'score': score
        })

    resultados.sort(key=lambda x: x['score'], reverse=True)
    top_resultados = resultados[:args.top]

    print(f"\nTop {args.top} funciones más similares a '{objetivo_nombre}':")
    for i, res in enumerate(top_resultados, 1):
        print(f"{i}. {res['archivo']} -> {res['nombre']} (Similitud: {res['score']:.2f})")

if __name__ == '__main__':
    iniciar_buscador()