import pytest
import json
import os
from unittest.mock import mock_open, patch
from src.file_handler import FileHandler, FileHandlerJSON  # замените your_module на имя вашего модуля


class TestFileHandler:
    """Тесты для абстрактного класса FileHandler"""

    def test_file_handler_is_abstract(self):
        """Тест, что FileHandler является абстрактным классом"""
        with pytest.raises(TypeError):
            FileHandler("test.json")

    def test_file_handler_has_abstract_methods(self):
        """Тест, что FileHandler имеет абстрактные методы"""
        assert hasattr(FileHandler, 'add_vacancy')
        assert hasattr(FileHandler, 'get_vacancies')
        assert FileHandler.add_vacancy.__isabstractmethod__
        assert FileHandler.get_vacancies.__isabstractmethod__


class TestFileHandlerJSON:
    """Тесты для класса FileHandlerJSON"""

    @pytest.fixture
    def sample_vacancies_data(self):
        """Фикстура с примером данных вакансий"""
        return {
            "items": [
                {
                    "name": "Python Developer",
                    "city": "Москва",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
                    "experience": "1-3 года",
                    "url": "https://hh.ru/vacancy/123"
                },
                {
                    "name": "Data Scientist Стажер",
                    "city": "Санкт-Петербург",
                    "salary": None,
                    "experience": "нет опыта",
                    "url": "https://hh.ru/vacancy/456"
                },
                {
                    "name": "Java Developer",
                    "city": "Москва",
                    "salary": {"from": 120000, "to": 180000, "currency": "RUB"},
                    "experience": "3-6 лет",
                    "url": "https://hh.ru/vacancy/789"
                }
            ]
        }

    @pytest.fixture
    def sample_vacancies_json(self, sample_vacancies_data):
        """Фикстура с JSON строкой вакансий"""
        return json.dumps(sample_vacancies_data)

    @pytest.fixture
    def file_handler(self, tmp_path):
        """Фикстура для создания FileHandlerJSON с временным файлом"""
        test_file = tmp_path / "vacancies.json"
        return FileHandlerJSON(str(test_file))

    def test_file_handler_json_inheritance(self):
        """Тест, что FileHandlerJSON наследуется от FileHandler"""
        assert issubclass(FileHandlerJSON, FileHandler)

    def test_file_handler_json_instantiation(self, tmp_path):
        """Тест создания экземпляра FileHandlerJSON"""
        test_file = tmp_path / "vacancies.json"
        handler = FileHandlerJSON(str(test_file))

        assert isinstance(handler, FileHandlerJSON)
        assert handler._FileHandler__filename == str(test_file)

    def test_file_handler_json_default_filename(self):
        """Тест создания экземпляра с filename по умолчанию"""
        handler = FileHandlerJSON()
        assert handler._FileHandler__filename == './data/vacancies.json'

    def test_get_vacancies_file_not_exists(self, file_handler):
        """Тест получения вакансий при отсутствии файла"""
        result = file_handler.get_vacancies()
        assert result == []

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_empty_file(self, mock_exists, mock_file, file_handler):
        """Тест получения вакансий из пустого файла"""
        mock_file.return_value.read.return_value = '{}'

        result = file_handler.get_vacancies()
        assert result == {}

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_without_criteria(self, mock_exists, mock_file, file_handler, sample_vacancies_json):
        """Тест получения всех вакансий без критериев"""
        mock_file.return_value.read.return_value = sample_vacancies_json

        result = file_handler.get_vacancies()

        assert isinstance(result, dict)
        assert 'items' in result
        assert len(result['items']) == 3

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_with_name_criteria(self, mock_exists, mock_file, file_handler, sample_vacancies_json):
        """Тест фильтрации вакансий по имени"""
        mock_file.return_value.read.return_value = sample_vacancies_json

        result = file_handler.get_vacancies(name="Стажер")

        assert len(result) == 1
        assert result[0]['name'] == "Data Scientist Стажер"

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_with_city_criteria(self, mock_exists, mock_file, file_handler, sample_vacancies_json):
        """Тест фильтрации вакансий по городу"""
        mock_file.return_value.read.return_value = sample_vacancies_json

        result = file_handler.get_vacancies(city="Москва")

        assert len(result) == 2
        assert all(vacancy['city'] == 'Москва' for vacancy in result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_with_multiple_criteria(self, mock_exists, mock_file, file_handler, sample_vacancies_json):
        """Тест фильтрации вакансий по нескольким критериям"""
        mock_file.return_value.read.return_value = sample_vacancies_json

        result = file_handler.get_vacancies(city="Москва", name="Python")

        assert len(result) == 1
        assert result[0]['name'] == "Python Developer"
        assert result[0]['city'] == "Москва"

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_no_matches(self, mock_exists, mock_file, file_handler, sample_vacancies_json):
        """Тест фильтрации вакансий без совпадений"""
        mock_file.return_value.read.return_value = sample_vacancies_json

        result = file_handler.get_vacancies(name="NonExistentPosition")

        assert result == []

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_partial_match(self, mock_exists, mock_file, file_handler, sample_vacancies_json):
        """Тест частичного совпадения при фильтрации"""
        mock_file.return_value.read.return_value = sample_vacancies_json

        result = file_handler.get_vacancies(name="Developer")

        assert len(result) == 2
        assert all("Developer" in vacancy['name'] for vacancy in result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_case_sensitivity(self, mock_exists, mock_file, file_handler, sample_vacancies_json):
        """Тест чувствительности к регистру при фильтрации"""
        mock_file.return_value.read.return_value = sample_vacancies_json

        result = file_handler.get_vacancies(name="python")

        assert len(result) == 0  # Должно быть 0, так как "Python" с большой буквы

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_with_empty_items(self, mock_exists, mock_file, file_handler):
        """Тест обработки файла с пустым items"""
        empty_data = {'items': []}
        mock_file.return_value.read.return_value = json.dumps(empty_data)

        result = file_handler.get_vacancies(name="Python")
        assert result == []

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_get_vacancies_malformed_json(self, mock_exists, mock_file, file_handler):
        """Тест обработки некорректного JSON"""
        mock_file.return_value.read.return_value = 'invalid json'

        with pytest.raises(json.JSONDecodeError):
            file_handler.get_vacancies()

    def test_add_vacancy_not_implemented(self, file_handler):
        """Тест, что add_vacancy не реализован"""
        with pytest.raises(NotImplementedError):
            file_handler.add_vacancy({})

    def test_update_vacancy_not_implemented(self, file_handler):
        """Тест, что update_vacancy не реализован"""
        with pytest.raises(NotImplementedError):
            file_handler.update_vacancy()

    def test_delete_vacancy_not_implemented(self, file_handler):
        """Тест, что delete_vacancy не реализован"""
        with pytest.raises(NotImplementedError):
            file_handler.delete_vacancy()


@pytest.mark.integration
class TestFileHandlerJSONIntegration:
    """Интеграционные тесты с реальными файлами"""

    def test_get_vacancies_with_real_file(self, tmp_path):
        """Тест с реальным файлом"""
        test_file = tmp_path / "test_vacancies.json"
        test_data = {
            "items": [
                {"name": "Test Developer", "city": "Test City"},
                {"name": "Another Test", "city": "Another City"}
            ]
        }

        # Создаем реальный файл
        with open(test_file, 'w') as f:
            json.dump(test_data, f)

        # Тестируем
        handler = FileHandlerJSON(str(test_file))
        result = handler.get_vacancies(name="Test")

        assert len(result) == 1
        assert result[0]['name'] == "Test Developer"

    def test_get_vacancies_file_not_exists_integration(self, tmp_path):
        """Интеграционный тест с несуществующим файлом"""
        test_file = tmp_path / "non_existent.json"
        handler = FileHandlerJSON(str(test_file))

        result = handler.get_vacancies()
        assert result == []

        # Проверяем, что файл не был создан
        assert not os.path.exists(test_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])