import json
from abc import ABC, abstractmethod
import os
from src.vacancy import Vacancy


class FileHandler(ABC):
    def __init__(self, filename):
        self.__filename = filename

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass


class FileHandlerJSON(FileHandler):
    def __init__(self, filename='./data/vacancies.json'):
        super().__init__(filename)
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _read_file(self):
        """Чтение данных из файла"""
        if not os.path.exists(self._FileHandler__filename):
            return {'items': []}

        try:
            with open(self._FileHandler__filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {'items': []}

    def _write_file(self, data):
        """Запись данных в файл"""
        with open(self._FileHandler__filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy):
        """Добавление вакансии в файл с проверкой на дубликаты"""
        data = self._read_file()

        # Проверяем, существует ли вакансия с таким ID
        existing_ids = {item.get('id') for item in data['items']}
        if vacancy.id in existing_ids:
            return False  # Вакансия уже существует

        # Добавляем новую вакансию
        data['items'].append(vacancy.to_dict())
        self._write_file(data)
        return True

    def add_vacancies(self, vacancies):
        """Добавление списка вакансий"""
        data = self._read_file()
        existing_ids = {item.get('id') for item in data['items']}

        added_count = 0
        for vacancy in vacancies:
            if vacancy.id not in existing_ids:
                data['items'].append(vacancy.to_dict())
                existing_ids.add(vacancy.id)
                added_count += 1

        self._write_file(data)
        return added_count

    def get_vacancies(self, **criteria):
        """Получение вакансий из файла с фильтрацией"""
        data = self._read_file()
        vacancies = [Vacancy.from_dict(item) for item in data['items']]

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                vacancy_value = getattr(vacancy, key, None)
                if vacancy_value is None or str(value).lower() not in str(vacancy_value).lower():
                    match = False
                    break
            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy_id):
        """Удаление вакансии по ID"""
        data = self._read_file()
        initial_count = len(data['items'])

        data['items'] = [item for item in data['items'] if item.get('id') != vacancy_id]

        if len(data['items']) < initial_count:
            self._write_file(data)
            return True
        return False

    def clear_all(self):
        """Очистка всех вакансий"""
        self._write_file({'items': []})