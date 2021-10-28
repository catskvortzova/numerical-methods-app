from tkinter import *

import numpy as np
from tkinter import messagebox as mb
import os
from tkinter import ttk
import tkinter
from NumericalMethods import EulerMethod,ImprovedEulerMethod,RungeKuttaMethod
from tkinter import messagebox
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import math
from math import sqrt

def dfdx(x,y):
    return math.sqrt((y-x)/x) + 1

def f(x,x0,y0):
    c = [
        (-1 * math.sqrt(x0) - math.sqrt(y0 - x0)) / (y0 - 2 * x0),
        (-1 * math.sqrt(x0) + math.sqrt(y0 - x0)) / (y0 - 2 * x0),
        ][0]

    return x * (-2/(c*sqrt(x)) + 1/(c**2 * x)+ 2)

class App:

    def __init__(self,master):

        super().__init__()
        self.master = master
        self.master.title("DiffSolver")
        self.master.geometry("824x624")
        self.master.resizable(width=False, height=False)

        self.canvas = Canvas(self.master, height=512, width=512)

        self.methods_names = ["Euler’s method", "Improved Euler’s method", "Runge-Kutta method"]
        self.little_methods_names = ["E", "IE", "RK"]

        self.labels = {}
        self.init_ui()
        self.tabs_count = 0
        self.saved_data = []


    def init_ui(self):

        notebook = ttk.Notebook(self.master,width=750, height = 500,padding = 0.001)
        notebook.place(x = 30,y = 80)

        self.labels['notebook'] = notebook
        self.create_main_tab()

        equation_text_field = Label(self.master, text = "Equation f(x,y) = ((y-x)/x)^(1/2) + 1", font=('Helvetica', 18, 'bold'))
        equation_text_field.place(x = 30, y = 10)

        y0_text = Label(self.master, text = "y0", font = ("A",13,'bold'))
        y0_text.place(x = 405, y = 50)

        y0_field = Entry(self.master, width = 3 ,bd = 1)
        y0_field.place(x = 400,y = 25)
        self.labels['y0_field'] = y0_field

        x0_text = Label(self.master, text = "x0", font = ("A",13,'bold'))
        x0_text.place(x = 445, y = 50)

        x0_field = Entry(self.master, width = 3 ,bd = 1)
        x0_field.place(x = 440,y = 25)
        self.labels['x0_field'] = x0_field

        x_text = Label(self.master, text = "x", font = ("A",13,'bold'))
        x_text.place(x = 490, y = 50)
        x_field = Entry(self.master, width = 3 ,bd = 1)
        x_field.place(x = 480,y = 25)
        self.labels['x_field'] = x_field

        n_text = Label(self.master, text = "n", font = ("A",13,'bold'))
        n_text.place(x = 530, y = 50)
        n_field = Entry(self.master, width = 3 ,bd = 1)
        n_field.place(x = 520,y = 25)
        self.labels['n_field'] = n_field

        n0_text = Label(self.master, text = "n0", font = ("A",13,'bold'))
        n0_text.place(x = 610, y = 50)
        n0_field = Entry(self.master, width = 3 ,bd = 1)
        n0_field.place(x = 605,y = 25)
        self.labels['n0_field'] = n0_field

        N_text = Label(self.master, text = "N", font = ("A",13,'bold'))
        N_text.place(x = 655, y = 50)
        N_field = Entry(self.master, width = 3 ,bd = 1)
        N_field.place(x = 645,y = 25)
        self.labels['N_field'] = N_field

        chose_method_text = Label(self.master, text = "Select method", font="A")
        chose_method_text.place(x = 30, y = 40)

        methods_chose = ttk.Combobox(self.master, values = self.methods_names, state="readonly")
        methods_chose.place(x = 150,y = 40)
        self.labels['methods_chose'] = methods_chose

        add_method_btn = Button(self.master, text = 'Add method', command  = lambda :[self.method_adding()], height = 1, width = 10)
        add_method_btn.place(x = 30,y = 80)
        self.labels['add_method_btn'] = add_method_btn

    def create_main_tab(self):

        new_frame = Frame()

        fig = Figure(figsize = (7.5, 10), dpi = 80)
        canvas = FigureCanvasTkAgg(fig, master = new_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        self.labels['notebook'].add(new_frame, text = "Comparison")
        self.labels['main tab'] = new_frame
        self.labels['main tab canvas'] = canvas


    def parse_float_field(self,field):
        data = self.labels[field].get()
        try:
            data = float(data)
            return data
        except:
            return None

    def check_fields(self):
        y0 = self.parse_float_field('y0_field')
        x0 = self.parse_float_field('x0_field')
        x = self.parse_float_field('x_field')
        n = self.parse_float_field('n_field')
        n0 = self.parse_float_field('n0_field')
        N = self.parse_float_field('N_field')

        if y0 is None:
            messagebox.showinfo('Not correct value','Please enter correct y0!')
            return 0,None,None,None,None,None,None
        elif x0 is None:
            messagebox.showinfo('Not correct value','Please enter correct x0!')
            return 0,None,None,None,None,None,None
        elif x is None:
            messagebox.showinfo('Not correct value','Please enter correct x!')
            return 0,None,None,None,None,None,None
        elif n is None:
            messagebox.showinfo('Not correct value','Please enter correct n!')
            return 0,None,None,None,None,None,None
        elif n0 is None:
            messagebox.showinfo('Not correct value','Please enter correct n0!')
            return 0,None,None,None,None,None,None
        elif N is None:
            messagebox.showinfo('Not correct value','Please enter correct N!')
            return 0,None,None,None,None,None,None

        return 1,y0,x0,x,n,n0,N

    def solve(self,name,y0,x0,x,n,n0,N):
        if name == "Euler’s method":
            method = EulerMethod(x0,y0,x,n,n0,N,dfdx,f)
        elif name == "Improved Euler’s method":
            method = ImprovedEulerMethod(x0,y0,x,n, n0,N,dfdx,f)
        else:
            method = RungeKuttaMethod(x0,y0,x,n,n0,N,dfdx,f)
        method.eval()
        data = method.get_data()
        return data

    def draw_new_solution(self,data,method_name,title_method):

        new_frame = Frame()

        fig = Figure(figsize = (13, 10), dpi = 60)

        solution_plot = fig.add_subplot(211)
        solution_plot.plot(data['xs'],data['y_exact'])
        solution_plot.plot(data['xs'],data['y_method'])
        solution_plot.title.set_text(data['title'])

        lte_plot = fig.add_subplot(223)
        lte_plot.plot(data['lte'])
        lte_plot.title.set_text('LTE')

        gte_plot = fig.add_subplot(224)
        gte_plot.plot([i for i in range(data['n0'],data['N'])],data['gte'])
        gte_plot.title.set_text('Total error for n from {} to {}'.format(data['n0'],data['N']))

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master = new_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        self.labels['notebook'].add(new_frame, text = title_method)
        self.labels['frame_' + str(self.tabs_count)] = new_frame
        self.tabs_count+=1

    def update_main_tab(self):
        frame = self.labels['main tab']

        fig = Figure(figsize = (13, 10), dpi = 60)

        solution_plot = fig.add_subplot(211)
        solution_plot.plot(self.saved_data[0]['xs'],self.saved_data[0]['y_exact'])

        legends = []
        for data in self.saved_data:
            solution_plot.plot(data['xs'],data['y_method'],label = data['title'])
            legends.append(data['title'])
        solution_plot.legend(['Exact solution'] + legends, loc='upper right')

        legends = []
        lte_plot = fig.add_subplot(223)
        for data in self.saved_data:
            lte_plot.plot(data['lte'],label = data['title'])
            legends.append(data['title'])
        lte_plot.legend(legends, loc='upper right')
        lte_plot.title.set_text('LTE')

        legends = []
        gte_plot = fig.add_subplot(224)
        for data in self.saved_data:
            t = 'Total error {} for n from {} to {}'.format(data['title'],data['n0'],data['N'])
            gte_plot.plot([i for i in range(data['n0'],data['N'])],data['gte'],label = t)
            legends.append(t)
        gte_plot.legend(legends, loc='upper right')


        gte_plot.title.set_text('Total error')

        fig.tight_layout()

        for widget in frame.winfo_children():
            widget.destroy()


        frame.pack_forget()

        canvas = FigureCanvasTkAgg(fig, master = frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


    def method_adding(self):

        s,y0,x0,x,n,n0,N = self.check_fields()
        if s == 0: return 0
        if self.labels['methods_chose'].current() == -1:
            messagebox.showinfo('','Please select a method!')
            return 0

        method_name = self.labels['methods_chose'].get()
        title_method = self.little_methods_names[self.labels['methods_chose'].current()]

        data = self.solve(method_name,y0,x0,x,n,n0,N)
        data['title'] = method_name + (" for n = {}".format(data['n']))

        self.saved_data.append(data)
        self.update_main_tab()

        self.draw_new_solution(data,method_name,title_method)

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()





