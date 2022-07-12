from random import randint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class LayoutGraph:
    def __init__(self, grafo, iters, refresh, c1, c2, verbose=False):
        """
        Parámetros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        c1: constante de repulsión
        c2: constante de atracción
        verbose: si está encendido, activa los comentarios
        """

        # Guardo el grafo
        self.grafo = grafo
        self.cant_vert = len(grafo[0])

        # Inicializo estado
        self.posiciones = self._init_positions()
        self.fuerzas = {}

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2
        
        self.plt_fig, self.plt_ax = plt.subplots(subplot_kw={'aspect': 'equal'})

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        pass
    
    def _init_positions(self):
        pos = dict()
        vert = self.grafo[0]

        for v in vert:
            x = randint(1, 2 * self.cant_vert)
            y = randint(1, 2 * self.cant_vert)
            
            pos[v] = (x, y)

        return pos

    def plot(self):
        #for v in self.grafo[0]:
        #    xy = self.posiciones[v]
        #    circ = plt.Circle(xy=xy, radius=0.5)
        #    self.plt_ax.add_patch(circ)
        #    self.plt_ax.text(x=xy[0], y=xy[1], s=v, horizontalalignment='center', verticalalignment='center')
        x = [xc for xc, yc in self.posiciones.values()]
        y = [yc for xc, yc in self.posiciones.values()]

        plt.scatter(x, y, 1000)
        for v in self.grafo[0]:
            xy = self.posiciones[v]
            self.plt_ax.text(x=xy[0], y=xy[1], s=v, horizontalalignment='center', verticalalignment='center')

        for e in self.grafo[1]:
            x1, y1 = self.posiciones[e[0]]
            x2, y2 = self.posiciones[e[1]]
            plt.plot((x1, x2), (y1, y2), 'gray')

        self.plt_ax.set_xlim(0, 2*self.cant_vert+1)
        self.plt_ax.set_ylim(0, 2*self.cant_vert+1)

        plt.show()
