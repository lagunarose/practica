try:
    import psycopg2
except:
    print('Не установлена библиотека psycopg2!')

class DataBase:

    #При создании экземпляра создаем подключение
    def __init__(self, PROJECT_SETTINGS):

        db = PROJECT_SETTINGS.get('database')
        db_name = db.get('database')
        db_host = db.get('host')
        db_user = db.get('user')
        db_pass = db.get('password')
        db_port = db.get('port', 5432)

        self.__conn = psycopg2.connect(dbname=db_name, host=db_host, user=db_user, password=db_pass, port=db_port)
        self.__cursor = self.__conn.cursor()
    
    #Чтобы закрыть соединение
    def stop_bd(self):
        self.__cursor.close()
        self.__conn.close()
    


    #### PROCEDURES
    def User_insert(self, IP:str, Login:str, Password:str):
        self.__cursor.execute("call User_insert(%s, %s, %s)", (IP, Login, Password))
        self.__conn.commit()
        return self.clear_notice(self.__conn.notices[-1])

    def User_update(self, IP:str, Login:str, Password:str):
        self.__cursor.execute("call User_update(%s, %s, %s)", (IP, Login, Password))
        self.__conn.commit()
        return self.clear_notice(self.__conn.notices[-1])

    def User_drop(self, IP:str):
        self.__cursor.execute("call User_drop(%s)", (IP, ))
        self.__conn.commit()
        return self.clear_notice(self.__conn.notices[-1])

    def Logs_insert(self, Logs:list):
        self.__cursor.executemany("call Logs_insert(%s, %s, %s)", Logs)
        self.__conn.commit()
        return self.clear_notice(self.__conn.notices[-1])
    


    #### FUNCTIONS
    def User_check_reg(self, Login:str, Password:str):
        self.__cursor.execute("select * from Users_check_registreted(%s, %s)", (Login, Password))
        return self.transform_list(self.__cursor.fetchall())
    
    def User_is_registreted(self, Login:str, Password:str):
        self.__cursor.execute("select * from Users_is_registreted(%s, %s)", (Login, Password))
        return self.transform_list(self.__cursor.fetchall())
    
    def Logs_sort_IP(self, IP:str):
        self.__cursor.execute("select * from Logs_sort_IP(%s)", (IP, ))
        return self.transform_list(self.__cursor.fetchall())
    
    def Logs_sort_date(self, IP:str, Date:str):
        self.__cursor.execute("select * from Logs_sort_date(%s, %s)", (IP, Date))
        return self.transform_list(self.__cursor.fetchall())
    
    def Logs_sort_dates(self, IP:str, Date1:str, Date2:str):
        self.__cursor.execute("select * from Logs_sort_dates(%s, %s, %s)", (IP, Date1, Date2))
        return self.transform_list(self.__cursor.fetchall())
    


    ### убрать \n
    def clear_notice(self, notice):
        #return [i.rstrip('\n') for i in notices]
        return notice.rstrip('\n')

    ###to list
    def transform_list(self, list_data):
        return [i[0] for i in list_data]

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.join(sys.path[0], "../"))
    try:
        from settings import PROJECT_SETTINGS
    except:
        print('Файл settings.py не найден!')

    db = DataBase(PROJECT_SETTINGS)

    #print(db.User_insert('', 'Admin1', 'Iv!12341234'))

    # res = db.Logs_sort_IP('::1')
    # print(res)

    # res = db.Logs_sort_date('::1', '23/06/2023')
    # print(res)

    # res = db.Logs_sort_dates('::1', '23/06/2023', '23/07/2023')
    # print(res)

    res = db.User_check_reg('ISS', 'qQQQ#####111')
    print(res)

    res = db.User_is_registreted('ISS', 'qQQQ#####111')
    print(res)

    db.stop_bd()
