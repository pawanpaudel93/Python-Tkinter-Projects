from tkinter import *
from tkinter import ttk


class CGProject:
    label1 = ''
    common_chars = ''

    def __init__(self, window):
        self.style = ttk.Style()
        self.style.configure("TButton", font="Helvetica 10", foreground='black', background='blue', padding=10)
        self.window = window
        self.window.title('Text1')
        # self.window.geometry('420x340')
        self.window.configure(bg='grey')
        Label(window, text="Enter Text1", bg='red').grid(row=0, sticky=W)
        self.label_entry1 = Text(self.window, height=10)
        self.label_entry1.grid(row=1, column=0, columnspan=4)
        ttk.Button(self.window, text='SAVE', command=lambda: self.create_next()).grid(row=2, column=0, sticky=W)
        # window.bind('<Return>', lambda event: self.create_next())

    def create_next(self):
        window1 = Tk()
        window1.title('Text2')
        # window1.geometry('420x340')
        window1.configure(bg='grey')
        self.style.configure("TButton", font="Serif 10", foreground='black', background='blue', padding=10)
        Label(window1, text="Enter Text2", bg='red').grid(row=0, sticky=W)
        label_entry2 = Text(window1, height=10)
        label_entry2.grid(row=1, columnspan=4)
        self.label1 = label_entry2
        Button(window1, text='COMPARE', fg='black', bg='blue', font="Helvetica 10", height=2, relief=SUNKEN, command=lambda: self.final(window1)).grid(row=2, column=0, sticky=W)
        # window1.bind('<Return>', lambda event: self.final(window1))

    def final(self, window1):
        window2 = Tk()
        # window2.geometry('420x340')
        window2.title('Result')
        window2.configure(bg='grey')
        content1 = self.label_entry1.get('1.0', "end-1c")
        content2 = self.label1.get('1.0', "end-1c")
        self.save_file('text1.txt', content1)
        self.save_file('text2.txt', content2)
        text1 = str(self.open_file('text1.txt'))
        text2 = str(self.open_file('text2.txt'))
        words1 = str(len(text1.split()))
        words2 = str(len(text2.split()))
        len1 = len(text1)
        len2 = len(text2)
        common = self.common_characters(text1, text2)
        total1 = text1 + ': ' + '\nCharacters-' + str(len1) + ' Words-' + words1 + '\n' \
                 + 'Unique Characters: ' + str(self.unique_characters(text1))
        total2 = text2 + ':' + '\nCharacters-' + str(len2) + ' Words-' + words2 + '\n' \
                 + 'Unique Characters: ' + str(self.unique_characters(text2))
        total3 = "\n Common Characters are:" + str(common)
        if text1 == text2:
            Label(window2, text='SAME TEXT').pack()
        else:
            Label(window2, text='MISMATCH').pack()
        Label(window2, text='Comparison', bg='maroon', fg='black').pack(fill=X)
        Label(window2, text=total1, bg='red', fg='black').pack(fill=X)
        Label(window2, text=total2, bg='green', fg='black').pack(fill=X)
        Label(window2, text=total3, bg='blue', fg='black').pack(fill=X)
        ttk.Button(window2, text='CloseAll', command=lambda: self.exit(window1, window2)).pack()
        ttk.Button(window2, text='Try Again!!', command=lambda: self.try_again(window1, window2)).pack()

    def exit(self, window1, window2):
        self.window.destroy()
        window1.destroy()
        window2.destroy()

    def try_again(self, window1, window2):
        # self.window.destroy()
        window1.destroy()
        window2.destroy()
        CGProject(self.window)

    def save_file(self, file_name, file_content):
        with open(file_name, 'w') as o:
            o.write(file_content)
            o.close()

    def open_file(self, file_name):
        with open(file_name, 'r') as file:
            return file.read()

    def common_characters(self, text1, text2):
        common = ''
        common_list = list(set(text1) & set(text2))
        for chars in common_list:
            if chars.isspace():
                continue
            common += chars + ', '
        common = common[0:len(common) - 2]
        self.common_chars = common_list
        return common

    def unique_characters(self, text):
        uncommon = ''
        for a in text:
            if a in self.common_chars or a.isspace() or a in uncommon:
                pass
            else:
                uncommon += a + ', '
        uncommon = uncommon[0:len(uncommon) - 2]
        return uncommon


root = Tk()
project = CGProject(root)
root.mainloop()
