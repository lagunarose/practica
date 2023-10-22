class Application:

    def __init__(self, mode, parser, db):
        self.__mode = mode
        self.__parser = parser
        self.__db = db
        self.__user_IP = ''
        self.__user_role = ''

    def show_message(self, *msg):
        if self.__mode == 'string':
            print(*msg)

    def register_user(self):
        self.show_message('\n\n\t\tРегистрация\n\n')
        while True:
            IP = input('Введите IP: ')
            Login = input('Введите Логин: ')
            Password = input('Введите Пароль: ')


            notice = self.__db.User_insert(IP=IP, Login=Login, Password=Password)

            if notice == 'ЗАМЕЧАНИЕ:  Все прошло успешно':
                self.show_message('Пользователь успешно зарегистрирован.')
                break
            else:
                self.show_message(notice, '\nПопробуйте изменить входные данные.')

                answer = input('Хотите ли Вы авторизироваться? (y - для авторизации): ').strip()
                if answer == 'y':
                    self.auth_user()
                    break

        self.__user_IP = IP
        self.__check_IP()
    
    def auth_user(self):
        self.show_message('\n\n\t\tАвторизация\n\n')
        while True:
            Login = input('Введите Логин: ')
            Password = input('Введите Пароль: ')

            answer = self.__db.User_is_registreted(Login=Login, Password=Password)
            
            if len(answer) > 0:
                self.__user_IP = answer[0]

                self.show_message('Авторизация прошла успешно.')
                break

            else:
                self.show_message('Данный пользователь не найден.')

                answer = input('Хотите ли Вы зарегистрировать нового пользователя? (y - для регистрации): ').strip()
                if answer == 'y':
                    self.register_user()
                    break


        self.__check_IP()


    def __check_IP(self):
        IP = self.__user_IP
        if bool(re.match(r".*[0-9]*", IP)) and len(IP) == 15:
            self.__user_role = 'admin'
        else:
            self.__user_role = 'user'
    

    def choose_option(self):
        if self.__user_role == 'admin':
            self.__choose_option_admin()
        else:
            self.__choose_option_user()
    

    def __choose_option_admin(self):
        while True:
            answer = input('Выберите действие:\n1.Выборка по IP.\n2.Выборка по IP и дате.\n3.Выборка по IP и временному промежутку\nq - завершить работу.\n\nДействие:').strip()

            match answer:
                case '1':
                    self.__Logs_sort_IP_admin()
                case '2':
                    self.__Logs_sort_date_admin()
                case '3':
                    self.__Logs_sort_dates_admin()
                    
                case 'q':
                    sys.exit()
                case _:
                    self.show_message('Введен неверный символ!\n')


    def __Logs_sort_IP_admin(self):
        self.show_message('\n\n\t\tВыборка по IP\n\n')


        IP = input('Введите IP для выборки\n(Оставьте поле1 пустым для просмотра всех логов): ').rstrip()
        IP = IP if len(IP) > 0 else self.__user_IP

        logs = self.__db.Logs_sort_IP(IP=IP)

        self.show_message('\n\nРезультат:\n', self.__to_table(logs), '\n\n\n')


    def __Logs_sort_date_admin(self):
        self.show_message('\n\n\t\tВыборка по дате\n\n')
        
        IP = input('Введите IP для выборки\n(Оставьте поле пустым для просмотра всех логов): ').rstrip()
        IP = IP if len(IP) > 0 else self.__user_IP

        Date = input('Введите нужную вам дату для выборки в формате (дд/мм/гггг): ')
        
        answer = self.__db.Logs_sort_date(IP=IP, Date=Date)

        self.show_message('\n\nРезультат:\n', self.__to_table(answer), '\n\n\n')


    def __Logs_sort_dates_admin(self):
        self.show_message('\n\n\t\tВыборка по временному промежутку\n\n')

        IP = input('Введите IP для выборки\n(Оставьте поле пустым для просмотра всех логов): ').rstrip()
        IP = IP if len(IP) > 0 else self.__user_IP

        Date1 = input('Введите начальную дату для выборки в формате (дд/мм/гггг): ')
        Date2 = input('Введите конечную дату для выборки в формате (дд/мм/гггг): ')
        
        answer = self.__db.Logs_sort_dates(IP=self.__user_IP, Date1=Date1, Date2=Date2)

        self.show_message('\n\nРезультат:\n', self.__to_table(answer), '\n\n\n')

    def __choose_option_user(self):
        while True:
            answer = input('Выберите действие:\n1.Вывести все Ваши логи.\n2.Выборка Ваших логов по дате.\n3.Выборка Ваших логов по временному промежутку.\nq - завершить работу.\n\nДействие:').strip()

            match answer:
                case '1':
                    self.__Logs_sort_IP_user()
                case '2':
                    self.__Logs_sort_date_user()
                case '3':
                    self.__Logs_sort_dates_user()
                    
                case 'q':
                    sys.exit()
                case _:
                    self.show_message('Введен неверный символ!\n')


    def __Logs_sort_IP_user(self):
        self.show_message('\n\n\t\tВывод всех IP\n\n')

        logs = self.__db.Logs_sort_IP(IP=self.__user_IP)

        self.show_message('\n\nРезультат:\n', self.__to_table(logs), '\n\n\n')


    def __Logs_sort_date_user(self):
        self.show_message('\n\n\t\tВыборка по дате\n\n')

        Date = input('Введите нужную вам дату для выборки в формате (дд/мм/гггг): ')
        
        answer = self.__db.Logs_sort_date(IP=self.__user_IP, Date=Date)

        self.show_message('\n\nРезультат:\n', self.__to_table(answer), '\n\n\n')


    def __Logs_sort_dates_user(self):
        self.show_message('\n\n\t\tВыборка по временному промежутку\n\n')

        Date1 = input('Введите начальную дату для выборки в формате (дд/мм/гггг): ')
        Date2 = input('Введите конечную дату для выборки в формате (дд/мм/гггг): ')
        
        answer = self.__db.Logs_sort_dates(IP=self.__user_IP, Date1=Date1, Date2=Date2)

        self.show_message('\n\nРезультат:\n', self.__to_table(answer), '\n\n\n')


    def __to_table(self, data):
        table = ''

        for row in data:
            table+= row + '\n'
        
        return table
            
            






if __name__ == '__main__':
    import re
    import sys
    try:
        from settings import PROJECT_SETTINGS
    except:
        print('Не найден файл settings.py в корневой директории проекта!')
    
    try:
        from Database.database import DataBase
    except:
        print('Не надйен файл database.py в папке Database корневой директории!')
    
    try:
        from Parser.parser import Parser
    except:
        print('Не надйен файл parser.py в папке Parser корневой директории!')

    parser = Parser(PROJECT_SETTINGS)
    db = DataBase(PROJECT_SETTINGS)

    app = Application('string', parser, db)

    while True:
        
        answer = input('Для авторизации нажмите 1, для регистрации нажмите 2: (1/2): ').strip()

        if answer == '2':
            app.register_user()
            break
        elif answer == '1':
            app.auth_user()
            break

    while True:
        app.choose_option()

    
    print('Не упала!')
else:
    app = Application('string')

#user_practica