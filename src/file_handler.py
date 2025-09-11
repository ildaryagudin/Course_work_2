import json
from abc import ABC, abstractmethod
import os
from pprint import pprint

class FileHandler:
    def __init__(self, filename):
        self.__filename = filename

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        pass


class FileHandlerJSON(FileHandler):
    def __init__(self, filename='./data/vacancies.json'):
        super().__init__(filename)

    def get_vacancies(self, **criteria):
        """Получение вакансии из файла"""
        if not os.path.exists(self._FileHandler__filename):
            return []
        with open(self._FileHandler__filename, 'r') as f:
            vacancies = json.load(f)

        if criteria:
            filtered_vacancies = []
            for vacancie in vacancies.get('items'):
                for key, value in criteria.items():
                    if value in vacancie.get(key):
                        filtered_vacancies.append(vacancie)
            return filtered_vacancies
        return vacancies

    def add_vacancy(self, vacancy):
        """Добавление вакансии в файл"""
        pass

    def update_vacancy(self):
        """Обновление вакансии в файле"""
        pass

    def delete_vacancy(self):
        """Удаление вакансии из файла"""
        pass



if __name__ == "__main__":
    file_handler = FileHandlerJSON()
    vacancies = file_handler.get_vacancies(name="Стажер")
    print(vacancies)

