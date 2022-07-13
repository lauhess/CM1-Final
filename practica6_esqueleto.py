#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse

import parser
from layout import LayoutGraph

def main():
    # Definimos los argumentos de linea de comando que aceptamos
    arg_parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    arg_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    arg_parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=50
    )
    # Temperatura inicial
    arg_parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )
    # Archivo del cual leer el grafo
    arg_parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = arg_parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    print(args.verbose)
    print(args.iters)
    print(args.file_name)
    print(args.temp)

    grafo = parser.read_graph(args.file_name)
    layout = LayoutGraph(grafo, iters=args.iters, refresh=1, c1=0.1, c2=5.0, verbose=args.verbose)
    layout.layout()

    return

    # # TODO: Borrar antes de la entrega
    # grafo1 = ([1, 2, 3, 4, 5, 6, 7],
    #           [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])
    #
    # # Creamos nuestro objeto LayoutGraph
    # layout_gr = LayoutGraph(
    #     grafo1,  # TODO: Cambiar para usar grafo leido de archivo
    #     iters=args.iters,
    #     refresh=1,
    #     c1=0.1,
    #     c2=5.0,
    #     verbose=args.verbose
    # )
    #
    # # Ejecutamos el layout
    # layout_gr.layout()
    # return


if __name__ == '__main__':
    main()
