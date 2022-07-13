import matplotlib.pyplot as plt
import numpy as np


class LayoutGraph:
    def __init__(self, grafo, iters, temp, refresh, c1, c2, verbose=False, width=200, height=200):
        """
        Parámetros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        temp: temperatura inicial
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        c1: constante de repulsión
        c2: constante de atracción
        verbose: si está encendido, activa los comentarios
        """

        # Guardo el grafo
        self.grafo = grafo
        self.cant_vert = len(grafo[0])
        
        self.vert2idx = {grafo[0][i]:i for i in range(self.cant_vert)}

        # Inicializo estado
        self.posiciones = np.empty((self.cant_vert, 2)) 
        self.fuerzas = np.empty((self.cant_vert, 2))

        # Guardo opciones
        self.iters = iters
        self.temp = temp
        self.verbose = verbose
        self.refresh = refresh
        self.c1 = c1    # Constante de atracción
        self.c2 = c2    # Constante de repulsión
        self.c3 = 0.95  # Constante de cambio de temperatura
        
        self.width = width
        self.height = height

        self._init_positions()
        self._draw()

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        for _ in range(self.iters):
            self._step()
            self._draw()

    def _step(self):
        self._initialize_accumulators()
        self._compute_attraction_forces()
        self._compute_repulsion_forces()
        self._compute_gravity_forces()
        self._update_positions()
        self._update_temperature()
    
    def _idx(self, v):
        return self.vert2idx[v]

    def _init_positions(self):
        self.posiciones = np.random.rand(self.cant_vert, 2)
        self.posiciones[:,0] *= self.width
        self.posiciones[:,1] *= self.height

    def _get_vertex_pos(self, v):
        return self.posiciones[self._idx(v)]

    def _initialize_accumulators(self):
        self.fuerzas = np.zeros((self.cant_vert, 2))

    def _compute_attraction_forces(self):
        for (orig, dest) in self.grafo[1]:
            diff = self._get_vertex_pos(dest) - self._get_vertex_pos(orig)
            dist = np.linalg.norm(diff)

            mod_f = self.f_attraction(dist, self.c1)
            f_xy = (mod_f / dist) * diff

            self.fuerzas[self._idx(orig)] += f_xy
            self.fuerzas[self._idx(dest)] -= f_xy

    def _compute_repulsion_forces(self):
        for v_i in self.grafo[0]:
            for v_j in self.grafo[0]:
                if v_i != v_j:
                    diff = self._get_vertex_pos(v_j) - self._get_vertex_pos(v_i)
                    dist = np.linalg.norm(diff)

                    mod_f = self.f_repulsion(dist, self.c2)
                    f_xy = (mod_f / dist) * diff

                    self.fuerzas[self._idx(v_i)] += f_xy
                    self.fuerzas[self._idx(v_j)] -= f_xy
    
    def _compute_gravity_forces(self):
        for v in self.grafo[0]:
            center = (self.height // 2, self.width // 2)
            pos = self._get_vertex_pos(v)

            diff = center - pos
            dist = np.linalg.norm(diff)

            mod_f = self.f_gravity(dist, self.c1)
            f_xy = (mod_f / dist) * diff

            self.fuerzas[self._idx(v)] += f_xy

    def _update_positions(self):
        for v in self.grafo[0]:
            vec_f = self.fuerzas[self._idx(v)]
            norm_f = np.linalg.norm(vec_f)
            if norm_f > self.temp:
                vec_f = (self.temp / norm_f) * vec_f
                #self._fuerzas[self._idx(v)] = vec_f
            self.posiciones[self._idx(v)] += vec_f

    def _draw(self, wait=0.2):
        plt.pause(wait)
        plt.cla()

        for v in self.grafo[0]:
            x, y = self._get_vertex_pos(v) 
            plt.scatter(x, y, 1000, c="lightblue")

        for (orig, dest) in self.grafo[1]:
            p_orig =  self._get_vertex_pos(orig)
            p_dest =  self._get_vertex_pos(dest)

            x = [p_orig[0], p_dest[0]]
            y = [p_orig[1], p_dest[1]]
            plt.plot(x, y, color="gray")

        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

        plt.draw()

    def _update_temperature(self):
        self.temp *= self.c3

    @staticmethod
    def f_attraction(d, k):
        return (d**2) / k

    @staticmethod
    def f_repulsion(d, k):
        return (k**2) / d
    
    @classmethod
    def f_gravity(cls, d, k):
        return 0.1 * cls.f_attraction(d, k)

