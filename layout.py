from random import randint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import vector

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

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2
        self.fuerzas = self.fr_v1()
        
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

    def f_attraction(d):
        return d**2 / k
    
    def f_repulsion(d):
        return k**2 / d
    
    def forces_compute(self, v_i, v_j, accum_x, accum_y, force_apply):
        p_i = self.posiciones[v_i]
        p_j = self.posiciones[v_j]
    
        dist = vector.dist(p_i, p_j)
        mod_fa = force_apply(dist)
        
        fx = mod_fa * (p_j[0] - p_i[0]) / dist
        fy = mod_fa * (p_j[1] - p_i[1]) / dist
    
        accum_x[v_i] += f_x
        accum_y[v_i] += f_y
        accum_x[v_j] -= f_x
        accum_y[v_j] -= f_y

    def fr_v1(self):
        accum = dict()
        for i in range(1, self.iters+1):
            for v in self.grafo[0]:
                accum[v] = 0

            for e in self.grafo[1]:
                p_orig = self.posiciones[e[0]]
                p_dest = self.posiciones[e[1]]
                f = vector.dist(p_orig, p_dest)

                accum[e[0]] += f
                accum[e[1]] -= f

            for v_i in self.grafo[0]:
                for v_j in self.grafo[0]:
                    p_i = self.posiciones[v_i]
                    p_j = self.posiciones[v_j]
                    if (p_i != p_j):
                        f = vector.dist(p_i, p_j)
        
                        accum[e[0]] += f
                        accum[e[1]] -= f

        print(accum)
        return accum

    def fr_v2(self):
        accum_x = dict()
        accum_y = dict()
        for i in range(1, self.iters+1):
            # Inicializar acumuladores
            for v in self.grafo[0]:
                accum_x[v] = 0
                accum_y[v] = 0

            # Computar fuerzas de attración
            for e in self.grafo[1]:
                self.forces_compute(e[0], e[1], accum_x, accum_y, f_attraction)

            # Computar fuerzas de repulsión
            for v_i in self.grafo[0]:
                for v_j in self.grafo[1]:
                    if (v_i != v_j):
                        self.forces_compute(v_i, v_j, accum_x, accum_y, f_repulsion)

            # Actualizar posiciones
            for v in self.grafo[0]:
                p_v = self.posiciones[v]
                self.posiciones[v] = vector.sum(p_v, (accum_x[v], accum_y[v]))

