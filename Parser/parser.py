try:
    from apachelogs import LogParser
except:
    print('Не установлен apachelogs!')

class Parser:

    __formats = ['%a', '%{c}a', '%A', '%B', '%b', '%D', '%f', '%h', '%{c}h', '%H',
                 '%k', '%l', '%L', '%m', '%p', '%P', '%q', '%r', '%R', '%s', '%>s', '%t', '%T',
                 '%u', '%U', '%v', '%V', '%X']

    def __init__(self, PROJECT_SETTINGS) -> None:
        
        self.__path = PROJECT_SETTINGS.get('log_file').get('path')
        self.__mask = PROJECT_SETTINGS.get('log_file').get('mask')

    def parsing(self):

        rows = []

        parser = LogParser(self.__mask)

        with open(self.__path) as file:
            for log in file.readlines():
                line = parser.parse(log)

                ip = line.remote_host
                date = line.request_time.strftime("%d/%m/%Y")
                log = log.rstrip('\n')

                row = (ip, date, log)

                rows.append(row)
        
        return rows

    # def __fill_dict(self, content):
    #     formats = self.__formats

    #     format_dict = {}

    #     for format in formats:
    #         znach = content.get(format, None)
    #         if znach is None:
    #             znach = ''
    #         format_dict[format] = str(znach)
        
    #     return format_dict

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.join(sys.path[0], "../"))
    sys.path.append(os.path.join(sys.path[0], "../Database/"))
    try:
        from settings import PROJECT_SETTINGS
    except:
        print('Файл парсер забран из семьи((\nИли файл main.py в корневой папке проекта удален.')
    
    try:
        from database import DataBase
    except:
        print('Файл парсер забран из семьи((\nИли папка Database в корневой папке проекта удалена.')
    
    parser = Parser(PROJECT_SETTINGS)

    db = DataBase(PROJECT_SETTINGS)

    res = db.Logs_insert(parser.parsing())
    count = 0
    for notice in res:
        if notice == 'ЗАМЕЧАНИЕ:  Все прошло успешно':
            count += 1
    
    if count:
        print(f'Добавлен {count} логов в БД')
    else:
        print(f'Новых логов не обнаружено')