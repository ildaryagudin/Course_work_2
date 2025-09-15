import pytest
import json
import os
import tempfile
from src.file_handler import FileHandlerJSON
from src.vacancy import Vacancy


class TestFileHandlerJSON:
    @pytest.fixture
    def temp_file(self):
        """Фикстура для создания временного файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"items": []}')
            temp_filename = f.name

        yield temp_filename

        # Удаляем временный файл после теста
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

    @pytest.fixture
    def sample_vacancies(self):
        """Фикстура для создания тестовых вакансий"""
        return [
            Vacancy(
                name="Python Developer",
                city="Москва",
                url="https://hh.ru/vacancy/1",
                salary={"from": 100000, "to": 150000, "currency": "RUR"},
                vacancy_id="1"
            ),
            Vacancy(
                name="Java Developer",
                city="Санкт-Петербург",
                url="https://hh.ru/vacancy/2",
                salary={"from": 120000, "to": 180000, "currency": "RUR"},
                vacancy_id="2"
            ),
            Vacancy(
                name="Data Scientist",
                city="Москва",
                url="https://hh.ru/vacancy/3",
                salary=None,
                vacancy_id="3"
            )
        ]

    def test_init_creates_directory(self, temp_file):
        """Тест создания директории при инициализации"""
        directory = os.path.dirname(temp_file)
        if os.path.exists(directory):
            os.rmdir(directory)

        handler = FileHandlerJSON(temp_file)
        assert os.path.exists(directory)

    def test_add_vacancy(self, temp_file, sample_vacancies):
        """Тест добавления вакансии"""
        handler = FileHandlerJSON(temp_file)
        result = handler.add_vacancy(sample_vacancies[0])

        assert result is True

        # Проверяем, что вакансия добавлена
        vacancies = handler.get_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0].id == "1"

    def test_add_duplicate_vacancy(self, temp_file, sample_vacancies):
        """Тест добавления дубликата вакансии"""
        handler = FileHandlerJSON(temp_file)
        handler.add_vacancy(sample_vacancies[0])
        result = handler.add_vacancy(sample_vacancies[0])  # Пытаемся добавить ту же вакансию

        assert result is False

        # Проверяем, что вакансия не добавилась повторно
        vacancies = handler.get_vacancies()
        assert len(vacancies) == 1

    def test_add_vacancies(self, temp_file, sample_vacancies):
        """Тест добавления нескольких вакансий"""
        handler = FileHandlerJSON(temp_file)
        added_count = handler.add_vacancies(sample_vacancies)

        assert added_count == 3

        vacancies = handler.get_vacancies()
        assert len(vacancies) == 3

    def test_get_vacancies_empty(self, temp_file):
        """Тест получения вакансий из пустого файла"""
        handler = FileHandlerJSON(temp_file)
        vacancies = handler.get_vacancies()

        assert vacancies == []

    def test_get_vacancies_with_data(self, temp_file, sample_vacancies):
        """Тест получения вакансий из файла с данными"""
        handler = FileHandlerJSON(temp_file)
        handler.add_vacancies(sample_vacancies)

        vacancies = handler.get_vacancies()
        assert len(vacancies) == 3

    def test_get_vacancies_with_filter(self, temp_file, sample_vacancies):
        """Тест получения вакансий с фильтрацией"""
        handler = FileHandlerJSON(temp_file)
        handler.add_vacancies(sample_vacancies)

        # Фильтр по городу
        moscow_vacancies = handler.get_vacancies(city="Москва")
        assert len(moscow_vacancies) == 2

        # Фильтр по названию
        python_vacancies = handler.get_vacancies(name="Python")
        assert len(python_vacancies) == 1
        assert python_vacancies[0].name == "Python Developer"

    def test_delete_vacancy(self, temp_file, sample_vacancies):
        """Тест удаления вакансии"""
        handler = FileHandlerJSON(temp_file)
        handler.add_vacancies(sample_vacancies)

        # Удаляем вакансию
        result = handler.delete_vacancy("1")
        assert result is True

        vacancies = handler.get_vacancies()
        assert len(vacancies) == 2
        assert all(vac.id != "1" for vac in vacancies)

    def test_delete_nonexistent_vacancy(self, temp_file, sample_vacancies):
        """Тест удаления несуществующей вакансии"""
        handler = FileHandlerJSON(temp_file)
        handler.add_vacancies(sample_vacancies)

        result = handler.delete_vacancy("999")
        assert result is False

        vacancies = handler.get_vacancies()
        assert len(vacancies) == 3

    def test_clear_all(self, temp_file, sample_vacancies):
        """Тест очистки всех вакансий"""
        handler = FileHandlerJSON(temp_file)
        handler.add_vacancies(sample_vacancies)

        handler.clear_all()

        vacancies = handler.get_vacancies()
        assert vacancies == []

    def test_read_corrupted_file(self):
        """Тест чтения поврежденного файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"corrupted": data}')  # Невалидный JSON
            temp_filename = f.name

        try:
            handler = FileHandlerJSON(temp_filename)
            vacancies = handler.get_vacancies()

            # Должен вернуть пустой список при ошибке чтения
            assert vacancies == []
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)