import copy
from abc import ABCMeta, abstractmethod
import numpy as np

class NumericalMethod(metaclass=ABCMeta):
    def __init__(self, x0, y0, x, n, n0, N, equation, solution):

        self.x0 = float(x0)
        self.y0 = float(y0)
        self.x = float(x)

        self.n = int(n)
        self.n0 = int(n0)
        self.N = int(N)

        self.equation = equation
        self.solution = solution

        self.lte = []
        self.gte = []
        self.y_exact = []
        self.y_method = []
        self.xs = []

    @abstractmethod
    def method(self, h,xi,yi): pass

    def compute(self,n_current):
        xi = copy.copy(self.x0)
        yi = copy.copy(self.y0)

        h_current = (self.x - self.x0)/n_current

        xs = []
        y_exact = []
        y_method = []
        lte = []

        while (xi <= self.x + 0.000001):
            xs.append(float(xi))
            y_e = self.solution(float(xi),self.x0,self.y0)  # y exact
            y_exact.append(float(y_e))

            y_m = self.method(h_current,xi,yi)
            y_method.append(float(yi))

            lte.append(self.compute_lte(y_e, yi))


            yi = copy.copy(y_m)
            xi = float(h_current) + float(xi)


        return {
            'xs':list(xs),
            'y_exact':list(y_exact),
            'y_method':list(y_method),
            'lte':list(lte)
        }

    def eval(self):
        main_data = self.compute(self.n)

        self.xs = list(main_data['xs'])
        self.y_exact = list(main_data['y_exact'])
        self.y_method = list(main_data['y_method'])
        self.lte = list(main_data['lte'])

        for i in range(self.n0,self.N):
            gte_data = self.compute(i)
            current_lte = np.max(gte_data['lte'])
            self.gte.append(current_lte)

    def compute_lte(self, y_e, y_m):
        return abs(y_e - y_m)

    def change_params(self,x0, y0, x):
        self.x0 = float(x0)
        self.y0 = float(y0)
        self.x = float(x)
        self.clear_computing()

    def change_equations(self,equation, solution):
        self.equation = equation
        self.solution = solution
        self.clear_computing()

    def clear_computing(self):
        self.lte = []
        self.gte = []
        self.y_exact = []
        self.y_method = []
        self.xs = []


    def get_data(self):
        return {
            'x0':self.x0,
            'y0': self.y0,
            'x':self.x,
            'n': self.n,
            'n0':self.n0,
            'N':self.N,
            'xs': self.xs,
            'y_exact': self.y_exact,
            'y_method': self.y_method,
            'lte': self.lte,
            'gte': self.gte
        }


class EulerMethod(NumericalMethod):
    def method(self, h, xi, yi):
        return yi + h * self.equation(float(xi), float(yi))


class ImprovedEulerMethod(NumericalMethod):
    def method(self, h, xi, yi):
        return yi + h * self.equation(float(xi) + (h / 2),
                                           float(yi) + (h / 2) * self.equation(xi, yi))

class RungeKuttaMethod(NumericalMethod):
    def method(self, h, xi, yi):
        k1 = self.equation(xi, yi)
        k2 = self.equation(xi + (h / 2), yi + (h * k1) / 2)
        k3 = self.equation(xi + (h / 2), yi + (h * k2) / 2)
        k4 = self.equation(xi + h, yi + h * k3)
        y_rk = yi + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        return y_rk
