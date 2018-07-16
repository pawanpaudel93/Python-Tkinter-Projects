from tkinter import *
from tkinter import ttk
import math


class Calculator:
    equal_to = 0
    calc_value = 0.0
    div_trigger = False
    mult_trigger = False
    add_trigger = False
    sub_trigger = False
    root_trigger = False
    power_trigger = False
    divx_trigger = False
    cube_trigger = False
    # math_button_pressed_once = 0

    def __init__(self, window):
        self.label_entry_value = ''
        self.entry_value = StringVar(window, value="")
        window.title('Calculator')
        window.geometry('550x340')
        window.resizable(width=False, height=False)

        style = ttk.Style()
        style.configure("TButton", font="Serif 10", padding=10)
        style.configure("TEntry", font="Serif 10", padding=10)

        self.number_entry = ttk.Entry(window, textvariable=self.entry_value, width=65)
        self.number_entry.grid(row=1, columnspan=4)
        self.label_entry = ttk.Entry(window, text='')
        self.label_entry.grid(row=0, column=2, columnspan=2, sticky=E)
        Label(window, text="PAWAN's CALCULATOR", relief=RAISED).grid(row=0, column=0, columnspan=2, sticky=W)
        # --------- For Buttons Click ----------
        window.bind('/', lambda event: self.math_button_press(value='/'))
        window.bind('+', lambda event: self.math_button_press(value='+'))
        window.bind('-', lambda event: self.math_button_press(value='-'))
        window.bind('*', lambda event: self.math_button_press(value='*'))

        window.bind('1', lambda event: self.button_press(value='1'))
        window.bind('2', lambda event: self.button_press(value='2'))
        window.bind('3', lambda event: self.button_press(value='3'))
        window.bind('4', lambda event: self.button_press(value='4'))
        window.bind('5', lambda event: self.button_press(value='5'))
        window.bind('6', lambda event: self.button_press(value='6'))
        window.bind('7', lambda event: self.button_press(value='7'))
        window.bind('8', lambda event: self.button_press(value='8'))
        window.bind('9', lambda event: self.button_press(value='9'))
        window.bind('0', lambda event: self.button_press(value='0'))

        window.bind('<Return>', lambda event: self.equal_button_press())

        # -------- First Row --------

        self.button7 = ttk.Button(window, text="7", command=lambda: self.button_press('7')).grid(row=3, column=0)
        self.button8 = ttk.Button(window, text="8", command=lambda: self.button_press('8')).grid(row=3, column=1)
        self.button9 = ttk.Button(window, text="9", command=lambda: self.button_press('9')).grid(row=3, column=2)
        self.button_div = ttk.Button(window, text="/", command=lambda: self.math_button_press('/')).grid(row=3, column=3)

        # ------- Second Row ---------
        self.button4 = ttk.Button(window, text="4", command=lambda: self.button_press('4')).grid(row=4, column=0)
        self.button5 = ttk.Button(window, text="5", command=lambda: self.button_press('5')).grid(row=4, column=1)
        self.button6 = ttk.Button(window, text="6", command=lambda: self.button_press('6')).grid(row=4, column=2)
        self.button_mul = ttk.Button(window, text="*", command=lambda: self.math_button_press('*')).grid(row=4, column=3)

        # --------- Third Row -----------

        self.button1 = ttk.Button(window, text="1", command=lambda: self.button_press('1')).grid(row=5, column=0)
        self.button2 = ttk.Button(window, text="2", command=lambda: self.button_press('2')).grid(row=5, column=1)
        self.button3 = ttk.Button(window, text="3", command=lambda: self.button_press('3')).grid(row=5, column=2)
        self.button_add = ttk.Button(window, text="+", command=lambda: self.math_button_press('+')).grid(row=5, column=3)

        # -------- Fourth Row ---------

        self.button_clear = ttk.Button(window, text="AC", command=lambda: self.button_press('AC')).grid(row=6, column=0)
        self.button0 = ttk.Button(window, text="0", command=lambda: self.button_press('0')).grid(row=6, column=1)
        self.button_equal = ttk.Button(window, text="=", command=lambda: self.equal_button_press()).grid(row=6, column=2)
        self.button_sub = ttk.Button(window, text="-", command=lambda: self.math_button_press('-')).grid(row=6, column=3)

        # -------- Fifth Row ----------

        self.button_per = ttk.Button(window, text="√", command=lambda: self.one_button_press('r')).grid(row=7,
                                                                                                        column=0)
        self.button_per = ttk.Button(window, text="^", command=lambda: self.math_button_press('^')).grid(row=7, column=1)
        self.button_per = ttk.Button(window, text="1/x", command=lambda: self.one_button_press('1/x')).grid(row=7,
                                                                                                            column=2)
        self.button_per = ttk.Button(window, text="3√", command=lambda: self.one_button_press('c')).grid(row=7, column=3)

        # -------- sixth Row ------------------

        self.button_escape = ttk.Button(window, text='<--', command=lambda: self.button_escape_press()).grid(row=2,
                                                                                                             column=3)

    def button_press(self, value):
        if self.equal_to == 0:
            entry_val = self.number_entry.get()
            entry_val += value
            self.number_entry.delete(0, END)
            self.number_entry.insert(0, entry_val)

            if value == 'AC':
                # self.math_button_pressed_once = 0
                self.number_entry.delete(0, END)
                self.number_entry.insert(0, '')
        else:
            self.number_entry.delete(0, END)
            self.number_entry.insert(0, value)
            self.label_entry.delete(0, END)
            self.label_entry.insert(0, '')
            self.equal_to = 0

    def isfloat(self, str_val):
        try:
            float(str_val)
            return True
        except ValueError:
            return False

    def math_button_press(self, value):

        if self.isfloat(str(self.number_entry.get())):
            self.div_trigger = False
            self.mult_trigger = False
            self.add_trigger = False
            self.sub_trigger = False
            self.root_trigger = False
            self.power_trigger = False
            self.divx_trigger = False
            self.cube_trigger = False

            self.calc_value = float(self.entry_value.get())

            if value == '/':
                print("/ Pressed")
                self.div_trigger = True

            elif value == '*':
                print("* Pressed")
                self.mult_trigger = True

            elif value == '+':
                print("+ Pressed")
                self.add_trigger = True

            elif value == '^':
                self.power_trigger = True
                # self.math_button_pressed_once += 1
            else:
                print("- Pressed")
                self.sub_trigger = True

            self.number_entry.delete(0, END)
            self.label_entry.delete(0, END)
            self.label_entry_value = str(self.calc_value) + ' ' + value
            self.label_entry.insert(0, self.label_entry_value)

        else:
            self.number_entry.delete(0, END)
            self.number_entry.insert(0, 'ERROR')

    def one_button_press(self, value):
        if self.isfloat(str(self.number_entry.get())):
            self.div_trigger = False
            self.mult_trigger = False
            self.add_trigger = False
            self.sub_trigger = False
            self.root_trigger = False
            self.power_trigger = False
            self.divx_trigger = False
            self.cube_trigger = False

            self.calc_value = float(self.entry_value.get())
            if value == 'r':
                self.root_trigger = True
            elif value == '1/x':
                self.divx_trigger = True
            elif value == 'c':
                self.cube_trigger = True

            self.one_button_press_equal()
        else:
            self.number_entry.delete(0, END)
            self.number_entry.insert(0, 'ERROR')

    def one_button_press_equal(self):
        if self.root_trigger:
            solution = math.sqrt(self.calc_value)
        elif self.divx_trigger:
            solution = 1 / self.calc_value
        elif self.cube_trigger:
            solution = math.pow(self.calc_value, 1 / 3)

        self.number_entry.delete(0, END)
        self.number_entry.insert(0, solution)
        self.equal_to = 1

    def equal_button_press(self):
        if self.add_trigger or self.sub_trigger or self.mult_trigger or self.div_trigger or self.power_trigger:

            if self.add_trigger:
                solution = self.calc_value + float(self.entry_value.get())
            elif self.sub_trigger:
                solution = self.calc_value - float(self.entry_value.get())
            elif self.mult_trigger:
                solution = self.calc_value * float(self.entry_value.get())
            elif self.div_trigger:
                solution = self.calc_value / float(self.entry_value.get())
            elif self.power_trigger:
                solution = math.pow(self.calc_value, float(self.entry_value.get()))

            self.label_entry.delete(0, END)
            self.label_entry.insert(0, (self.label_entry_value + ' ' + str(float(self.entry_value.get()))))

            self.number_entry.delete(0, END)
            self.number_entry.insert(0, solution)
            self.equal_to = 1

    def button_escape_press(self):
        escape_press = self.entry_value.get()[:-1]
        self.number_entry.delete(0, END)
        self.number_entry.insert(0, escape_press)


root = Tk()
calculator = Calculator(root)
root.mainloop()
