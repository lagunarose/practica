from tkinter import *
from tkinter import ttk
import re
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
from tkinter.messagebox import OK, INFO, showinfo 

import sys
import os

sys.path.append(os.path.join(sys.path[0], "../"))
sys.path.append(os.path.join(sys.path[0], "../Database/"))
sys.path.append(os.path.join(sys.path[0], "../Parser/"))

try:
    from settings import PROJECT_SETTINGS
except:
    print('Файл интерфейс забран из семьи((\nИли файл settings.py в корневой папке проекта удален.')

try:
    from Database.database import DataBase
except:
    print('Файл интерфейс забран из семьи((\nИли папка Database в корневой папке проекта удалена.')

try:
    from Parser.parser import Parser
except:
    print('Файл интерфейс забран из семьи((\nИли папка Parser в корневой папке проекта удалена.')


class Main_window:
    
    def __init__(self, database, parser):

        self.__db = database
        self.__parser = parser

        self.__root = Tk()
        self.__root.title("Вход")
        self.__root.geometry("400x400+400+200")
        self.__root.resizable(False, False)
        btn_register_user = Button(text="Регистрация", command= self.__register_user)
        btn_auth_user = Button(text="Авторизация", command= self.__auth_user) 
        btn_register_user.place(width=80, height=40,x=160, y=100)
        btn_auth_user.place(width=80, height=40,x=160, y=200)
        self.__root.mainloop()

    def __register_user(self):
        self.__root.destroy()
        Register_window(self.__db, self.__parser)


    def __auth_user(self):
        self.__root.destroy()
        Auth_window(self.__db, self.__parser)

class Register_window:

    def __init__(self, database, parser):

        self.__db = database
        self.__parser = parser

        self.__register_window = Tk()
        self.__register_window.title("Регистрация")
        self.__register_window.geometry("400x400+400+200")
        self.__register_window.resizable(False, False)

        self.__register_window.columnconfigure(index=0, weight=2)
        self.__register_window.columnconfigure(index=1, weight=3)
        self.__register_window.columnconfigure(index=2, weight=2)
        self.__register_window.columnconfigure(index=3, weight=1)
        self.__register_window.columnconfigure(index=4, weight=2)
        self.__register_window.columnconfigure(index=5, weight=3)
        self.__register_window.columnconfigure(index=6, weight=2)

        self.__register_window.rowconfigure(index=0, weight=10)
        for r in range(1,8): self.__register_window.rowconfigure(index=r, weight=5)
        self.__register_window.rowconfigure(index=8, weight=10)

        label = Label(text="Введите следующие данные:", font=("Arial", 10), width=25)
        label.grid(column = 1, columnspan=5, row=1)

        label_I = Label(self.__register_window, text="IP: ")  
        label_I.grid(column=1, columnspan=2, row=2)  
        Entry_I = Entry(self.__register_window)  
        Entry_I.grid(column=4, columnspan=2, row=2)

        label_L = Label(self.__register_window, text="Login: ")  
        label_L.grid(column=1, columnspan=2, row=3)  
        Entry_L = Entry(self.__register_window)  
        Entry_L.grid(column=4, columnspan=2, row=3)

        label_P = Label(self.__register_window, text="Password: ")  
        label_P.grid(column=1, columnspan=2, row=4)  
        Entry_P = Entry(self.__register_window)  
        Entry_P.grid(column=4, columnspan=2, row=4)
        
        sumbit = Button(text='Продолжить', anchor='c', command= lambda : self.__sumbit_reg(Entry_I.get(),Entry_L.get(),Entry_P.get()))
        sumbit.grid(column=1, columnspan=5, row=7)

        button_bag = Button(master= self.__register_window, text='Вернуться назад', command = self.__bag__reg_window) 
        button_bag.grid(column = 0, columnspan=2, row = 0, sticky='nw')

    
    def __sumbit_reg(self, in_IP, Login, Password):

        notice = self.__db.User_insert(in_IP.strip(), Login, Password)

        if notice == 'ЗАМЕЧАНИЕ:  Все прошло успешно':
                result = askyesno(title='Регистрация прошла успешно', message='Хотите зарегать еще одного пользователя - Yes\nПерейти на страницу Авторизации - No')
                self.__register_window.destroy()
                if result:                  
                    Register_window(self.__db,self.__parser)
                else: 
                    Main_window(self.__db,self.__parser)
        else:
                showerror(title='Регистрация', message=f'{notice}')


        
    def __bag__reg_window(self):

        self.__register_window.destroy()
        Main_window(self.__db,self.__parser)




class Auth_window:

    def __init__(self, database, parser):

        self.__db = database
        self.__parser = parser

        self.__auth_window = Tk()
        self.__auth_window.title("Авторизация")
        self.__auth_window.geometry("400x400+400+200")
        label = Label(text="Введите следующие данные:", font=("Arial", 10), width=25)
        label.grid(column = 1, columnspan=5, row=1)
        self.__auth_window.resizable(False, False)

        self.__auth_window.columnconfigure(index=0, weight=2)
        self.__auth_window.columnconfigure(index=1, weight=3)
        self.__auth_window.columnconfigure(index=2, weight=2)
        self.__auth_window.columnconfigure(index=3, weight=1)
        self.__auth_window.columnconfigure(index=4, weight=2)
        self.__auth_window.columnconfigure(index=5, weight=3)
        self.__auth_window.columnconfigure(index=6, weight=2)

        self.__auth_window.rowconfigure(index=0, weight=10)
        for r in range(1,9): self.__auth_window.rowconfigure(index=r, weight=5)
        self.__auth_window.rowconfigure(index=10, weight=10)

        self.__errmsg_login = StringVar(value='Логин не может быть пустым')
        self.__errmsg_password = StringVar(value='Пароль не может быть пустым')
        
        check_L = (self.__auth_window.register(self.is_valid_Login), "%P")
        check_P = (self.__auth_window.register(self.is_valid_Password), "%P")

        label_L = Label(self.__auth_window, text="Login: ")  
        label_L.grid(column=1, columnspan=2, row=3)  
        self.__Entry_L = Entry(self.__auth_window, validate="key", validatecommand=check_L)  
        self.__Entry_L.grid(column=4, columnspan=2, row=3)

        error_label = ttk.Label(foreground="red", textvariable=self.__errmsg_login, wraplength=250)
        error_label.grid(column=4, columnspan=2, row=4)


        label_I = Label(self.__auth_window, text="Password: ")  
        label_I.grid(column=1, columnspan=2, row=5)  
        self.__Entry_I = Entry(self.__auth_window,validate="key", validatecommand=check_P)  
        self.__Entry_I.grid(column=4, columnspan=2, row=5)

        error_label = ttk.Label(foreground="red", textvariable=self.__errmsg_password, wraplength=250)
        error_label.grid(column=4, columnspan=2, row=6)

        
        submit = Button(text='Авторизироваться', anchor='c', command=self.sumbit)
        submit.grid(column=1, columnspan=5, row=7)

        button_bag = Button(master= self.__auth_window, text='Вернуться назад', command = self.__bag__auth_window) 
        button_bag.grid(column = 0, columnspan=6, row = 0, sticky='nw')


        
    def __bag__auth_window(self):

        self.__auth_window.destroy()
        Main_window(self.__db,self.__parser)

    def is_valid_Login(self, newval):
        result = False
        if len(newval) == 0:
            self.__errmsg_login.set('Логин не может быть пустым')
            result = True

        else:
            self.__errmsg_login.set('')
            result = True
        return result


    def is_valid_Password(self, newval):
        result = bool(re.search('[A-ZА-ЯЁ]*[!@#$%^&*\(\)\{\}]*[a-zа-яё]*', newval))
        if newval.rstrip() == '':
            self.__errmsg_password.set('Пароль не может быть пустым')
        elif not re.search('[A-ZА-ЯЁ]', newval):
            self.__errmsg_password.set('Пароль должен содержать заглавную букву')
        elif not re.search('[!@#$%^&*\(\)\{\}]', newval):
            self.__errmsg_password.set('Пароль должен содержать спец. символ')
        elif not re.search('[a-zа-яё]', newval):
            self.__errmsg_password.set('Пароль должен содержать прописную букву')
        elif len(newval) < 8:
            self.__errmsg_password.set('Пароль не должен быть меньше 8 символов')
        else:
            self.__errmsg_password.set('')
        return result

    

    def sumbit(self):
        Login = self.__Entry_L.get()
        Password = self.__Entry_I.get()

        if self.is_valid_Login(Login) and self.is_valid_Password(Password) and (len(Password) >= 8):
            
            answer = self.__db.User_is_registreted(Login=Login, Password=Password)

            if len(answer) > 0:

                self.__auth_window.destroy()
                Sort_Window(self.__db, self.__parser, answer[0])
                

            else:

                showerror(message="Пользователь не найден",default=OK)


class Sort_Window:

    def __init__(self, database, parser, user_IP):

        self.__db = database
        self.__parser = parser
        self.__user_IP = user_IP
        self.__check_IP()

        self.__sort_window = Tk()
        self.__construct_window()

        self.__sort_window.mainloop()

    def __construct_window(self):
        self.__sort_window.title("Выборка")
        self.__sort_window.geometry("400x400+400+200")
        self.__sort_window.resizable(False, False)

        self.__mask_grid()
        
        self.__choosed_IP()
        self.__bd_form.grid(column=1, row=5, sticky='nsew')
        


        label = Label(text="Выберите следующий вид сортировки из выпадающего списка", font=("Arial", 10))
        label.grid(column = 1, row=1)

        button_bag = Button(master= self.__sort_window, text='Вернуться назад', command = self.__bag__choosed_dates) 
        button_bag.grid(column = 0, columnspan=2, row = 0, sticky='nw')

        self.__create_func_choose()
        

    def __mask_grid(self):

        self.__sort_window.columnconfigure(index=0, weight=1, minsize=5)
        self.__sort_window.columnconfigure(index=1, weight=3, minsize=50)
        self.__sort_window.columnconfigure(index=2, weight=1, minsize=5)

        self.__sort_window.rowconfigure(index=0, weight=1, minsize=5)
        self.__sort_window.rowconfigure(index=1, weight=1, minsize=10)
        self.__sort_window.rowconfigure(index=2, weight=1, minsize=5)
        self.__sort_window.rowconfigure(index=3, weight=1, minsize=10)
        self.__sort_window.rowconfigure(index=4, weight=3, minsize=5)
        self.__sort_window.rowconfigure(index=5, weight=10, minsize=80)
        self.__sort_window.rowconfigure(index=6, weight=1, minsize=5)

    def __create_func_choose(self):
        role = self.__user_role

        self.__options = [
            "Выборка по IP" if role=='admin' else 'Показать все Ваши логи',
            "Выборка по IP и дате" if role=='admin' else 'Выборка Ваших логов по дате',
            "Выборка по IP и временному промежутку" if role=='admin' else 'Выборка Ваших логов по временному промежутку']
        self.__option_var = StringVar(value=self.__options[0])

        combobox = ttk.Combobox(master=self.__sort_window, textvariable=self.__option_var, values=self.__options, width=50)
        combobox.grid(column = 1, row=3)

        combobox.bind("<<ComboboxSelected>>", self.__selected_item_options)

        self.combobox_options = combobox


    def __selected_item_options(self, eventObject):
        option_var = self.combobox_options.get()
        options = self.__options

        self.__bd_form.destroy()

        if option_var == options[0]:
            self.__choosed_IP()

        elif option_var == options[1]:
            self.__choosed_date()

        elif option_var == options[2]:
            self.__choosed_dates()

        self.__bd_form.grid(column=1, row=5, sticky='nsew')
    

    def __choosed_IP(self):
        frame = ttk.Frame(master=self.__sort_window, height=1000, width=1000)

        frame.columnconfigure(index=0, weight=1)
        frame.columnconfigure(index=1, weight=1)
        frame.columnconfigure(index=2, weight=1)

        frame.rowconfigure(index=0, weight=1)
        frame.rowconfigure(index=1, weight=1)
        frame.rowconfigure(index=2, weight=1)

        if self.__user_role == 'admin':
            label_IP = Label(master=frame, text = 'Введите IP: ')
            label_IP.grid(column = 0 , row = 0)


            entry_IP = Entry(master=frame, width=45)
            entry_IP.grid(column=1, row = 0)

            entry_IP.insert('0', '  оставьте этот текст для отображения всех логов')
            entry_IP.bind("<FocusIn>", lambda args: entry_IP.delete('0', 'end') if entry_IP.get() == '  оставьте этот текст для отображения всех логов' else False)
            entry_IP.bind("<FocusOut>", lambda args: entry_IP.insert('0', '  оставьте этот текст для отображения всех логов') if entry_IP.get() == '' else False)

        button = Button(master=frame, text='Показать результат', command = lambda: self.__bd_sort_IP(entry_IP.get()) if self.__user_role == 'admin' else self.__bd_sort_IP(self.__user_IP)) 
        button.grid(column=0, columnspan=3, row=2)

        self.__bd_form = frame
        

    def __bd_sort_IP(self, in_IP):

        if in_IP == '  оставьте этот текст для отображения всех логов':

            in_IP = self.__user_IP
        
        db_data = self.__db.Logs_sort_IP(in_IP)

        if len(db_data) == 0:
            showinfo(title='Выборка по IP', message='Данного IP не найдено') 
        else:
            Answer_sort(db_data)



    def __choosed_date(self):
        frame = ttk.Frame()

        frame.columnconfigure(index=0, weight=1)
        frame.columnconfigure(index=1, weight=1)

        frame.rowconfigure(index=0, weight=1)
        frame.rowconfigure(index=1, weight=1)
        frame.rowconfigure(index=2, weight=1)

        if self.__user_role == 'admin':
            label_IP = Label(master=frame, text = 'Введите IP: ')
            label_IP.grid(column = 0 , row = 0)

            entry_IP = Entry(master=frame, width=45)
            entry_IP.grid(column=1, row = 0, sticky=W)

            entry_IP.insert('0', '  оставьте этот текст для отображения всех логов')
            entry_IP.bind("<FocusIn>", lambda args: entry_IP.delete('0', 'end') if entry_IP.get() == '  оставьте этот текст для отображения всех логов' else False)
            entry_IP.bind("<FocusOut>", lambda args: entry_IP.insert('0', '  оставьте этот текст для отображения всех логов') if entry_IP.get() == '' else False)

        label = Label(master=frame, text='Введите дату:')
        label.grid(column=0, row = 1)

        entry = ttk.Entry(master=frame, width=15)
        entry.grid(column=1, row = 1, sticky=W)

        entry.insert('0', 'dd/mm/yyyy')
        entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end') if entry.get() == 'dd/mm/yyyy' else False)
        entry.bind("<FocusOut>", lambda args: entry.insert('0', 'dd/mm/yyyy') if entry.get() == '' else False)

        button = Button(master=frame, text='Показать результат', command= lambda: self.__bd_sort_date(entry_IP.get(), entry.get()) if self.__user_role == 'admin' else self.__bd_sort_date(self.__user_IP, entry.get())) 
        button.grid(column=0, columnspan=2, row = 2)

        self.__bd_form = frame


    def __bd_sort_date(self, in_IP, date):

        if in_IP == '  оставьте этот текст для отображения всех логов':

            in_IP = self.__user_IP

        db_data = self.__db.Logs_sort_date(in_IP, date)

        if len(db_data) == 0:
            showinfo(title='Выборка по дате', message=f'Логов от {date} не найдено') 
        else:
            Answer_sort(db_data)

        



    def __choosed_dates(self):
        frame = ttk.Frame()

        frame.columnconfigure(index=0, weight=1)
        frame.columnconfigure(index=1, weight=1)
        frame.columnconfigure(index=2, weight=1)

        frame.rowconfigure(index=0, weight=1)
        frame.rowconfigure(index=1, weight=1)
        frame.rowconfigure(index=2, weight=1)
        frame.rowconfigure(index=3, weight=1)
        frame.rowconfigure(index=4, weight=1)

        if self.__user_role == 'admin':
            label_IP = Label(master=frame, text = 'Введите IP: ')
            label_IP.grid(column = 0 , row = 0, sticky=W)

            entry_IP = Entry(master=frame, width=45)
            entry_IP.grid(column=1, columnspan=2, row = 0)

            entry_IP.insert('0', '  оставьте этот текст для отображения всех логов')
            entry_IP.bind("<FocusIn>", lambda args: entry_IP.delete('0', 'end') if entry_IP.get() == '  оставьте этот текст для отображения всех логов' else False)
            entry_IP.bind("<FocusOut>", lambda args: entry_IP.insert('0', '  оставьте этот текст для отображения всех логов') if entry_IP.get() == '' else False)

        label = Label(master=frame, text='Введите начальную дату:')
        label.grid(column=0, columnspan=2, row = 1, sticky=W)

        entry1 = ttk.Entry(master=frame, width=15)
        entry1.grid(column = 2, row = 1, sticky=W)

        label = Label(master=frame, text='Введите конечную дату:')
        label.grid(column=0, columnspan=2, row = 2, sticky=W)

        entry2 = ttk.Entry(master=frame, width=15)
        entry2.grid(column = 2, row = 2, sticky=W)

        entry1.insert('0', 'dd/mm/yyyy')
        entry1.bind("<FocusIn>", lambda args: entry1.delete('0', 'end') if entry1.get() == 'dd/mm/yyyy' else False)
        entry1.bind("<FocusOut>", lambda args: entry1.insert('0', 'dd/mm/yyyy') if entry1.get() == '' else False)

        entry2.insert('0', 'dd/mm/yyyy')
        entry2.bind("<FocusIn>", lambda args: entry2.delete('0', 'end') if entry2.get() == 'dd/mm/yyyy' else False)
        entry2.bind("<FocusOut>", lambda args: entry2.insert('0', 'dd/mm/yyyy') if entry2.get() == '' else False)

        button = Button(master=frame, text='Показать результат', command = lambda : self.__bd_sort_dates(entry_IP.get(), entry1.get(), entry2.get()) if self.__user_role == 'admin' else self.__bd_sort_dates(self.__user_IP, entry1.get(), entry2.get())) 
        button.grid(column = 0, columnspan=3, row = 4)

        

        self.__bd_form = frame

    def __bag__choosed_dates(self):

        self.__sort_window.destroy()
        Main_window(self.__db,self.__parser)


        
    def __bd_sort_dates(self, in_IP, date1, date2):
        
        if in_IP == '  оставьте этот текст для отображения всех логов':

            in_IP = self.__user_IP
        print(in_IP, date1, date2)
        db_data = self.__db.Logs_sort_dates(in_IP, date1, date2)

        if len(db_data) == 0:
            showinfo(title='Выборка по промежутку времени', message=f'Логов в промежутке {date1} - {date2} не найдено') 
        else:
            Answer_sort(db_data)


    def __check_IP(self):
        IP = self.__user_IP
        if bool(re.match(r".*[0-9]*", IP)) and len(IP) == 15:
            self.__user_role = 'admin'
        else:
            self.__user_role = 'user'

    
class Answer_sort:

    def __init__(self, db_data = ['Нет данных']):
        self.__answer_sort = Tk()

        self.__answer_sort.title("Результат")
        self.__answer_sort.geometry("700x500")
        self.__answer_sort.resizable(False, False) 


        db_data_var = Variable(master=self.__answer_sort, value=db_data)
        listbox = Listbox(master=self.__answer_sort, listvariable=db_data_var)
        listbox.pack(side=LEFT, fill=BOTH, expand=1)
        
        scrollbar = ttk.Scrollbar(master=self.__answer_sort, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        listbox["yscrollcommand"]=scrollbar.set

        self.__answer_sort.mainloop()




Main_window(DataBase(PROJECT_SETTINGS), Parser(PROJECT_SETTINGS))

# Sort_Window(DataBase(PROJECT_SETTINGS), Parser(PROJECT_SETTINGS), '...............')

# Sort_Window(DataBase(PROJECT_SETTINGS), Parser(PROJECT_SETTINGS), '::1')


# data = ['::1 - - [23/Jun/2023:17:11:02 +0300] "GET / HTTP/1.1" 304 -', '::1 - - [23/Jun/2023:17:11:03 +0300] "GET / HTTP/1.1" 304 -', '::1 - - [23/Jun/2023:17:11:04 +0300] "GET / HTTP/1.1" 304 -',
# '::1 - - [23/Jun/2023:17:11:05 +0300] "GET / HTTP/1.1" 304 -', '::1 - - [23/Jun/2023:17:11:06 +0300] "GET / HTTP/1.1" 304 -',
# '::1 - - [23/Jun/2023:17:11:07 +0300] "GET / HTTP/1.1" 304 -', '::1 - - [23/Jun/2023:17:11:08 +0300] "GET / HTTP/1.1" 304 -',
# '::1 - - [23/Jun/2023:17:11:09 +0300] "GET / HTTP/1.1" 304 -', '::1 - - [23/Jun/2023:17:11:37 +0300] "-" 408 -']

# Answer_sort(data)
# Answer_sort()