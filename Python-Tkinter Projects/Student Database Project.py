import psycopg2
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk


class DatabaseProject:
    update_data_window = None
    data_show_window = None
    addData_Window = None

    def __init__(self, window):
        # connect database
        self.conn = psycopg2.connect("host='localhost' dbname='dbmsprojectt' user='postgres' password='admin'")
        self.curs = self.conn.cursor()
        try:
            pass
        except psycopg2.ProgrammingError:
            with self.conn as cursor:
                cursor.execute(open('student_schema.sql', 'r').read())


        # configure window, buttons and Entry
        window.title('StudentManagement')
        window.geometry('400x400')
        style = ttk.Style()
        style.configure("TButton", font="Serif 10", padding=10)
        style.configure("TEntry", font="Serif 10", padding=10)
        bottomFrame = Frame(window)
        bottomFrame.pack(side=BOTTOM)

        ttk.Label(window, text="Student List").pack()
        self.list_box = Listbox(window, selectmode=EXTENDED, width=50)
        self.list_box.pack()
        self.list_all()

        self.student_button = ttk.Button(window, text='Add Data', command=lambda: self.enter_data()).pack(side=LEFT)
        self.show_button = ttk.Button(window, text='Show Details', command=lambda: self.show_data()).pack(side=LEFT)
        self.delete_button = ttk.Button(window, text='Delete', command=lambda: self.delete_data()).pack(side=LEFT)
        self.update_button = ttk.Button(window, text='Update', command=lambda: self.update()).pack(side=LEFT)
        ttk.Button(bottomFrame, text='Close', command=lambda: self.close_connection(window)).pack()

    # list all data in listbox
    def list_all(self):
        self.curs.execute("""SELECT * FROM Student""")
        self.list_box.delete(0, END)
        rows = self.curs.fetchall()
        for row in rows:
            self.list_box.insert(0, str(row[0]) + ': ' + row[1] + ' ' + row[2] + ' ' + row[3])

    # delete data from database and listbox
    def delete_data(self):
        query = self.list_box.get(ACTIVE)
        if query:
            id = query[0]
            self.curs.execute("DELETE FROM Student WHERE studId=(%s)", (id,))
            self.conn.commit()
            self.list_box.delete(ACTIVE)
            messagebox.showinfo('Student Deleted', query + ' Student Deleted')

    # enter data on entry boxes
    def enter_data(self):
        self.addData_Window = Toplevel()
        # self.addData_Window.geometry('800x400')
        self.addData_Window.title('Add Student Data')

        self.curs.execute("""SELECT * FROM Student""")
        value = str(len(self.curs.fetchall()) + 1)

        ttk.Label(self.addData_Window, text='ID*').grid(row=1, column=0)
        self.id = ttk.Entry(self.addData_Window)
        self.id.grid(row=1, column=1)
        self.id.insert(0, value)

        ttk.Label(self.addData_Window, text='First Name').grid(row=2, column=0)
        self.first_name = ttk.Entry(self.addData_Window)
        self.first_name.grid(row=2, column=1)

        ttk.Label(self.addData_Window, text='Middle Name').grid(row=3, column=0)
        self.middle_name = ttk.Entry(self.addData_Window)
        self.middle_name.grid(row=3, column=1)

        ttk.Label(self.addData_Window, text='Last Name').grid(row=4, column=0)
        self.last_name = ttk.Entry(self.addData_Window)
        self.last_name.grid(row=4, column=1)

        ttk.Label(self.addData_Window, text='Address').grid(row=5, column=0)
        self.address = ttk.Entry(self.addData_Window)
        self.address.grid(row=5, column=1)

        ttk.Label(self.addData_Window, text='Phone No*').grid(row=6, column=0)
        self.phone_no = ttk.Entry(self.addData_Window)
        self.phone_no.grid(row=6, column=1)

        ttk.Label(self.addData_Window, text='DOB*').grid(row=7, column=0)
        self.dob = ttk.Entry(self.addData_Window)
        self.dob.grid(row=7, column=1)

        ttk.Label(self.addData_Window, text='Class').grid(row=8, column=0)
        self.class_name = ttk.Entry(self.addData_Window)
        self.class_name.grid(row=8, column=1)

        ttk.Label(self.addData_Window, text='Roll No').grid(row=9, column=0)
        self.roll_no = ttk.Entry(self.addData_Window)
        self.roll_no.grid(row=9, column=1)

        ttk.Label(self.addData_Window, text='Gender').grid(row=10, column=0)
        self.gender = ttk.Entry(self.addData_Window)
        self.gender.grid(row=10, column=1)

        ttk.Label(self.addData_Window, text='Upload Photo').grid(row=11, column=0)
        self.photo_button = ttk.Button(self.addData_Window, text='Browse', command=lambda: self.add_photo(self.addData_Window)).grid(row=11,
                                                                                                            column=1)
        self.photo_label = Label(self.addData_Window)
        self.photo_label.grid(row=12, column=1)

        self.add_button = ttk.Button(self.addData_Window, text='Add Data', command=lambda: self.add_data()).grid(row=13,
                                                                                                   column=1)
        ttk.Button(self.addData_Window, text='Close', command=lambda: self.addData_Window.destroy()).grid(row=14,
                                                                                                          column=1)

    # data add on the listbox and also on database
    def add_data(self):
        try:
            parameters = (self.id.get(), self.first_name.get(), self.middle_name.get(), self.last_name.get(),
                          self.address.get(), self.phone_no.get(), self.dob.get(), self.class_name.get(),
                          self.roll_no.get(), self.gender.get(), self.photo_label['text'].rstrip())
            print(self.photo_label['text'])
            self.curs.execute("INSERT INTO Student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", parameters)
            self.conn.commit()
            parameters = (self.id, self.first_name, self.middle_name, self.last_name, self.address, self.phone_no,
                          self.dob, self.class_name, self.roll_no, self.gender)
            for parameter in parameters:
                parameter.delete(0, END)
                parameter.insert(0, '')
            messagebox.showerror('Student Added', 'Student Added')
            self.list_all()
        except psycopg2.DataError as e:
            if self.conn:
                self.conn.rollback()
            messagebox.showinfo('Error', 'Please enter mandatory fields.')

    # show details of the student
    def show_data(self):
        self.data_show_window = Toplevel()
        # self.data_show_window.geometry('400x400')
        self.data_show_window.title('Student Details')
        frame = Frame(self.data_show_window, bd=2, relief=SUNKEN)
        frame.grid()

        query = self.list_box.get(ACTIVE)
        if not query:
            self.data_show_window.destroy()
        if query:    
            id = query[0]
            self.curs.execute("SELECT * FROM Student WHERE studId=(%s)", (id,))
            rows = self.curs.fetchall()
            for data in rows:
                if data[10]:
                    self.image = Image.open(data[10].rstrip())
                    resized = self.image.resize((200, 200), Image.ANTIALIAS)
                    self.photo = ImageTk.PhotoImage(resized)
                    label_image = Label(self.data_show_window, image=self.photo)
                    label_image.grid(row=0, column=1)

                ttk.Label(frame, text='ID*: ').grid(row=1, column=0)
                ttk.Label(frame, text=data[0]).grid(row=1, column=2)

                ttk.Label(frame, text='First Name: ').grid(row=2, column=0)
                ttk.Label(frame, text=data[1]).grid(row=2, column=2)

                ttk.Label(frame, text='Middle Name: ').grid(row=3, column=0)
                ttk.Label(frame, text=data[2]).grid(row=3, column=2)

                ttk.Label(frame, text='Last Name: ').grid(row=4, column=0)
                ttk.Label(frame, text=data[3]).grid(row=4, column=2)

                ttk.Label(frame, text='Address: ').grid(row=5, column=0)
                ttk.Label(frame, text=data[4]).grid(row=5, column=2)

                ttk.Label(frame, text='Phone No: ').grid(row=6, column=0)
                ttk.Label(frame, text=data[5]).grid(row=6, column=2)

                ttk.Label(frame, text='DOB*: ').grid(row=7, column=0)
                ttk.Label(frame, text=data[6]).grid(row=7, column=2)

                ttk.Label(frame, text='Class: ').grid(row=8, column=0)
                ttk.Label(frame, text=data[7]).grid(row=8, column=2)

                ttk.Label(frame, text='Roll No: ').grid(row=9, column=0)
                ttk.Label(frame, text=data[8]).grid(row=9, column=2)

                ttk.Label(frame, text='Gender: ').grid(row=10, column=0)
                ttk.Label(frame, text=data[9]).grid(row=10, column=2)

                ttk.Button(frame, text='Close', command=lambda: self.data_show_window.destroy()).grid(row=11,
                                                                                                column=1)
    
    # entry of data to update details of the student
    def update(self):
        self.update_data_window = Toplevel()
        self.update_data_window.title('Update Student')
        frame = Frame(self.update_data_window, bd=2, relief=SUNKEN)
        frame.grid()
        query = self.list_box.get(ACTIVE)
        if not query:
            self.update_data_window.destroy()
        self.studid = query[0]
        self.curs.execute("SELECT * FROM Student WHERE studId=(%s)", (self.studid,))
        rows = self.curs.fetchall()
        for data in rows:
            if data[10]:
                self.image = Image.open(data[10].rstrip())
                resized = self.image.resize((200, 200),Image.ANTIALIAS)
                self.photo = ImageTk.PhotoImage(resized)
                label_image = Label(self.update_data_window, image=self.photo)
                label_image.grid(row=0, column=1)
            
            ttk.Label(self.update_data_window, text='Upload Photo').grid(row=10, column=0)
            self.photo_label = ttk.Label(self.update_data_window, text=data[10])
            self.photo_label.grid(row=10, column=1)
            photo_button = ttk.Button(self.update_data_window, text='Browse', command=lambda: self.add_photo(self.update_data_window)).grid(row=1,
                                                                                                            column=1)
   
            ttk.Label(frame, text='ID*').grid(row=0, column=0)
            self.id1 = ttk.Label(frame)
            self.id1.grid(row=0, column=1)
            self.id1['text'] = data[0]

            ttk.Label(frame, text='First Name').grid(row=1, column=0)
            self.first_name1 = ttk.Entry(frame)
            self.first_name1.grid(row=1, column=1)
            self.first_name1.insert(0, data[1])

            ttk.Label(frame, text='Middle Name').grid(row=2, column=0)
            self.middle_name1 = ttk.Entry(frame)
            self.middle_name1.grid(row=2, column=1)
            self.middle_name1.insert(0, data[2])

            ttk.Label(frame, text='Last Name').grid(row=3, column=0)
            self.last_name1 = ttk.Entry(frame)
            self.last_name1.grid(row=3, column=1)
            self.last_name1.insert(0, data[3])

            ttk.Label(frame, text='Address').grid(row=4, column=0)
            self.address1 = ttk.Entry(frame)
            self.address1.grid(row=4, column=1)
            self.address1.insert(0, data[4])

            ttk.Label(frame, text='Phone No').grid(row=5, column=0)
            self.phone_no1 = ttk.Entry(frame)
            self.phone_no1.grid(row=5, column=1)
            self.phone_no1.insert(0, data[5])

            ttk.Label(frame, text='DOB*').grid(row=6, column=0)
            self.dob1 = ttk.Entry(frame)
            self.dob1.grid(row=6, column=1)
            self.dob1.insert(0, data[6])

            ttk.Label(frame, text='Class').grid(row=7, column=0)
            self.class_name1 = ttk.Entry(frame)
            self.class_name1.grid(row=7, column=1)
            self.class_name1.insert(0, data[7])

            ttk.Label(frame, text='Roll No').grid(row=8, column=0)
            self.roll_no1 = ttk.Entry(frame)
            self.roll_no1.grid(row=8, column=1)
            self.roll_no1.insert(0, data[8])

            ttk.Label(frame, text='Gender').grid(row=9, column=0)
            self.gender1 = ttk.Entry(frame)
            self.gender1.grid(row=9, column=1)
            self.gender1.insert(0, data[9])

        self.update_button = ttk.Button(frame, text='Update Data',
                                        command=lambda: self.update_data()).grid(row=11,
                                                                                 column=1)
        ttk.Button(self.update_data_window, text='Close', command=lambda: self.update_data_window.destroy()).grid(
            row=12,
            column=1)

    # update the details of the student on the list box and also database
    def update_data(self):
        update_values = (self.first_name1.get(), self.middle_name1.get(), self.last_name1.get(),
                         self.address1.get(), self.phone_no1.get(), self.dob1.get(), self.class_name1.get(),
                         self.roll_no1.get(), self.gender1.get(), self.photo_label['text'].rstrip(), self.studid)
        self.curs.execute("UPDATE Student SET first_name=%s, middle_name=%s, last_name=%s, address=%s, phone_no=%s, "
                          "dob=%s, class=%s, rollno=%s, gender=%s, photo=%s WHERE studId=%s", update_values)
        self.conn.commit()
        self.list_all()
        self.curs.execute("SELECT * FROM Student WHERE studId=(%s)", (self.studid,))
        rows = self.curs.fetchall()
        for data in rows:
            self.id1['text'] = ''
            self.id1['text'] = data[0]
            self.first_name1.delete(0, END)
            self.first_name1.insert(0, data[1])
            self.middle_name1.delete(0, END)
            self.middle_name1.insert(0, data[2])
            self.last_name1.delete(0, END)
            self.last_name1.insert(0, data[3])
            self.address1.delete(0, END)
            self.address1.insert(0, data[4])
            self.phone_no1.delete(0, END)
            self.phone_no1.insert(0, data[5])
            self.dob1.delete(0, END)
            self.dob1.insert(0, data[6])
            self.class_name1.delete(0, END)
            self.class_name1.insert(0, data[7])
            self.roll_no1.delete(0, END)
            self.roll_no1.insert(0, data[8])
            self.gender1.delete(0, END)
            self.gender1.insert(0, data[9])
            
            self.image = Image.open(data[10].rstrip())
            resized = self.image.resize((200, 200),Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(resized)

            label_image = Label(self.update_data_window, image=self.photo)
            label_image.grid(row=0, column=1)

            messagebox.showinfo('Student Updated',
                                self.first_name1.get() + self.middle_name1.get() + self.last_name1.get() + ' Updated')

    # close database connection
    def close_connection(self, window):
        self.curs.close()
        del self.curs
        self.conn.close()  # <--- Close the connection
        # if self.update_data_window or self.data_show_window or self.addData_Window:
        #     self.update_data_window.destroy()
        #     self.data_show_window.destroy()
        #     self.addData_Window.destroy()
        window.destroy()

    def add_photo(self, window):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.photo_label['text'] = filename
        
        self.image = Image.open(self.photo_label['text'].rstrip())
        resized = self.image.resize((200, 200),Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(resized)
        label_image = Label(window, image=self.photo)
        label_image.grid(row=0, column=1)


if __name__ == '__main__':
    root = Tk()
    data = DatabaseProject(root)
    root.mainloop()
