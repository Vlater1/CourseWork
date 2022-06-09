import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import messagebox as mbox

class MainWindow(tk.Frame):
    a = None
    b = None
    c = None
    d = None
    e = None
    f = None
    k = None
    def __init__(self, root):
        super().__init__(root)
        self.init_mainwindow()
    def init_mainwindow(self):
        btn_open_input_window = tk.Button(text="Ввести начальные данные", command = self.open_inputwindow, height = 10, width = 50, bg = 'white')
        btn_open_input_window.place(x = 150, y = 120)
        btn_open_result_window = tk.Button(text="Вычислить систему уравнений", command = self.open_resultwindow, height = 10, width = 50, bg = 'white')
        btn_open_result_window.place(x = 150, y = 370)
    def open_inputwindow(self):
        InputWindow()
    def open_resultwindow(self):
        if(self.a is None or self.b is None or self.c is None or self.d is None or self.e is None or self.f is None or self.k is None):
            mbox.showerror("Ошибка", "Не указаны исходные данные")
        else:
            system = OdeSolver(self.a, self.b, self.c, self.d, self.e, self.f, self.k)
            s = system.solve_ode(system.F(system.s0, system.t), system.s0, system.t)
            ResultWindow(s)
    def insert_data(self, a, b, c, d, e, f, k):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.k = k

class InputWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_inputwindow()
        self.view = app

    def init_inputwindow(self):
        self.title("Ввод начальных данных")
        self.geometry('350x350+100+100')

        label_a = tk.Label(self, text="a")
        label_a.place(x=100, y=50)
        label_b = tk.Label(self, text="b")
        label_b.place(x=100, y=80)
        label_c = tk.Label(self, text="c")
        label_c.place(x=100, y=110)
        label_d = tk.Label(self, text="d")
        label_d.place(x=100, y=140)
        label_e = tk.Label(self, text="e")
        label_e.place(x=100, y=170)
        label_f = tk.Label(self, text="f")
        label_f.place(x=100, y=200)
        label_k = tk.Label(self, text="k")
        label_k.place(x=100, y=230)
        self.entry_a = tk.Entry(self)
        self.entry_a.place(x=120, y=50)
        self.entry_b = tk.Entry(self)
        self.entry_b.place(x=120, y=80)
        self.entry_c = tk.Entry(self)
        self.entry_c.place(x=120, y=110)
        self.entry_d = tk.Entry(self)
        self.entry_d.place(x=120, y=140)
        self.entry_e = tk.Entry(self)
        self.entry_e.place(x=120, y=170)
        self.entry_f = tk.Entry(self)
        self.entry_f.place(x=120, y=200)
        self.entry_k = tk.Entry(self)
        self.entry_k.place(x=120, y=230)
        btn_cancel = tk.Button(self, text="Закрыть", command = self.destroy)
        btn_cancel.place(x=250, y=270)
        btn_add = tk.Button(self, text="Сохранить данные")
        btn_add.place(x=50, y=270)
        btn_add.bind('<Button-1>',lambda event: self.view.insert_data(self.entry_a.get(), self.entry_b.get(), self.entry_c.get(), self.entry_d.get(), self.entry_e.get(), self.entry_f.get(), self.entry_k.get()))
        self.grab_set()
        self.focus_set()


class ResultWindow(tk.Toplevel):
    def __init__(self, s):
        super().__init__(root)
        self.init_resultwindow()
    def init_resultwindow(self):
        self.title("Результат вычислений")
        self.geometry('800x800+100+100')
        At = tk.Frame(self, width=400, height=400)
        At.place(x=0, y=0)
        canvas = FigureCanvasTkAgg(s[0], At, label = "A(t)")
        canvas.show()
        canvas.get_tk_widget().pack()
        Et = tk.Frame(self, width=400, height=400)
        Et.place(x=400, y=400)
        canvas = FigureCanvasTkAgg(s[1], Et, label = "E(t)")
        canvas.show()
        canvas.get_tk_widget().pack()
        Bt = tk.Frame(self, width=400, height=400)
        Bt.place(x=400, y=0)
        canvas = FigureCanvasTkAgg(s[2], Bt, label="B(t)")
        canvas.show()
        canvas.get_tk_widget().pack()
        Ct = tk.Frame(self, width=400, height=400)
        Ct.place(x=0, y=400)
        canvas = FigureCanvasTkAgg(s[3], Ct, label="C(t)")
        canvas.show()
        canvas.get_tk_widget().pack()



class OdeSolver():
    t = np.linspace(0,20)
    s0 = [1.82, 78.719, 14.651, 3.624]
    def __init__(self, a, b, c, d, e, f, k):
        super().__init__()
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.k = k
    def F(self, s, t):
        dAdt = -k * s[0] * f - a * s[0] * s[2] * s[2] + b * s[3]
        dEdt = k * s[0] * f + c * s[1]
        dBdt = -2 * a * s[0] * s[2] * s[2] + 2 * b * s[3] + d - e * s[2]
        dCdt = a * s[0] * s[2] * s[2] - b * s[3]
        return [dAdt, dEdt, dBdt, dCdt]
    def solve_ode(self, F, s0, t):
        s = odeint(F, s0, t)
        return s



if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.title("Главное меню")
    root.geometry('800x800+100+100')
    root.mainloop()