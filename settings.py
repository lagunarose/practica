try:
    import yaml
except:
    print('Не установлен PyYaml!')

class Project_Settings():

    def __init__(self):
        with open('config.conf', 'r', encoding="utf8") as file:
            self.__data = yaml.safe_load(file)
    
    def get_data(self):
        return self.__data

if __name__ == '__main__':
    project_settings = Project_Settings()

    print(project_settings.get_data())

PROJECT_SETTINGS = Project_Settings().get_data()