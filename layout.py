from random import random
import matplotlib.pyplot as plt
import numpy as np
import math

PADDING_X = 50
PADDING_Y = 50

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
        self.fuerzas = np.zeros((self.cant_vert, 2))

        # Guardo opciones
        self.iters = iters
        self.temp = temp
        self.verbose = verbose
        self.refresh = refresh

        # Constantes
        self.c3 = 0.95  # Constante de cambio de temperatura
        self.epsilon = 0.01 
        
        self.width = width
        self.height = height
        self.dispersion = math.sqrt(self.width * self.height / self.cant_vert) 
        self.c1 = c1 * self.dispersion
        self.c2 = c2 * self.dispersion

        self._init_positions()
        plt.gca().set_aspect('equal') 
        self._draw()

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        for i in range(self.iters):
            if self.refresh != 0 and i % self.refresh == 0:
                self._draw()
            if self.temp < self.epsilon:
                # self.logger.notify_zero_temperature()
                break
            self._step()
        self._draw()
        plt.show()

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

            if dist < self.epsilon:
                self._logging_alert(f"{orig} y {dest} demasiado cerca")
                return 

            mod_f = self.f_attraction(dist, self.c2)
            f_xy = (mod_f / dist) * diff

            self.fuerzas[self._idx(orig)] += f_xy
            self.fuerzas[self._idx(dest)] -= f_xy

    def _compute_repulsion_forces(self):
        unused_vertices = list(self.grafo[0])

        while unused_vertices:
            v_i = unused_vertices.pop()
            for v_j in self.grafo[0]:
                if v_i != v_j:
                    diff = self._get_vertex_pos(v_j) - self._get_vertex_pos(v_i)
                    dist = np.linalg.norm(diff)

                    if dist < self.epsilon:
                        self._logging_alert(f"{v_i} y {v_j} demasiado cerca. Alejando")
                        theta = 2 * math.pi * random()
                        f_xy = np.array([math.cos(theta), math.sin(theta)])
                    else:
                        mod_f = self.f_repulsion(dist, self.c1)
                        f_xy = (mod_f / dist) * diff

                    self.fuerzas[self._idx(v_i)] -= f_xy
                    self.fuerzas[self._idx(v_j)] += f_xy
    
    def _compute_gravity_forces(self):
        for v in self.grafo[0]:
            center = (self.height // 2, self.width // 2)
            pos = self._get_vertex_pos(v)

            diff = center - pos
            dist = np.linalg.norm(diff)

            if dist < self.epsilon:
                return

            mod_f = self.f_gravity(dist, self.c1)
            f_xy = (mod_f / dist) * diff

            self.fuerzas[self._idx(v)] -= f_xy

    def _prevent_collision(self, v, mod):
        x, y = self.posiciones[self._idx(v)] + mod
        if x < 0 or x > self.width or y < 0 or y > self.height:
            self._logging_alert(f"{v} fuera de rango ({x}, {y})")
        if x < 0:
            x = (-x) % self.width
        elif x > self.width:
            x = self.width - x % self.width

        if y < 0:
            y = (-y) % self.height
        elif y > self.height:
            y = self.height - y % self.height

        self.posiciones[self._idx(v)] = np.array([x, y])
        
    def _update_positions(self):
        for v in self.grafo[0]:
            vec_f = self.fuerzas[self._idx(v)]
            norm_f = np.linalg.norm(vec_f)
            if norm_f > self.temp:
                vec_f = (self.temp / norm_f) * vec_f
                #self._fuerzas[self._idx(v)] = vec_f
            self._prevent_collision(v, vec_f)

    def _draw(self, wait=0.2):
        plt.pause(wait)
        plt.cla()

        for v in self.grafo[0]:
            x, y = self._get_vertex_pos(v) 
            plt.scatter(x, y, 500, c="lightblue")

        for (orig, dest) in self.grafo[1]:
            p_orig =  self._get_vertex_pos(orig)
            p_dest =  self._get_vertex_pos(dest)

            x = [p_orig[0], p_dest[0]]
            y = [p_orig[1], p_dest[1]]
            plt.plot(x, y, color="gray")

        plt.xlim(0 - PADDING_X, self.width + PADDING_X)
        plt.ylim(0 - PADDING_Y, self.height + PADDING_Y)
        plt.grid(visible=True)

        plt.draw()

    def _update_temperature(self):
        self.temp *= self.c3
        self._logging_value("Temperatura", self.temp)
    
    def _logging_value(self, var_name, value, indent=0):
        if self.verbose:
            ind = '\t' * indent
            print(f"{ind}[DEBUG] {var_name} = {value}")

    def _logging_alert(self, msg, indent=0):
        if self.verbose:
            ind = '\t' * indent
            print(f"{ind}[WARNING] {msg}")

    @staticmethod
    def f_attraction(d, k):
        return (d**2) / k

    @staticmethod
    def f_repulsion(d, k):
        return (k**2) / d
    
    @classmethod
    def f_gravity(cls, d, k):
        return 0.1 * cls.f_repulsion(d, k)

    

