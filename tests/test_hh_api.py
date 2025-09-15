import pytest
import requests
from unittest.mock import Mock, patch
from src.hh_api import hh_API
from src.vacancy import Vacancy


class TestHHAPI:
    @pytest.fixture
    def hh_api(self):
        """Фикстура для создания экземпляра API"""
        return hh_API()

    @pytest.fixture
    def mock_response(self):
        """Фикстура для мока ответа API"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {
                    'name': 'Python Developer',
                    'area': {'name': 'Москва'},
                    'url': 'https://hh.ru/vacancy/1',
                    'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
                    'id': '1'
                },
                {
                    'name': 'Java Developer',
                    'area': {'name': 'Санкт-Петербург'},
                    'url': 'https://hh.ru/vacancy/2',
                    'salary': {'from': 120000, 'to': 180000, 'currency': 'RUR'},
                    'id': '2'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        return mock_response

    def test_init(self, hh_api):
        """Тест инициализации API"""
        assert hh_api.session is not None
        assert isinstance(hh_api.session, requests.Session)

    @patch('requests.Session.get')
    def test_get_vacancies_success(self, mock_get, hh_api, mock_response):
        """Тест успешного получения вакансий"""
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies("Python", 2)

        assert len(vacancies) == 2
        assert all(isinstance(vac, Vacancy) for vac in vacancies)
        assert vacancies[0].name == "Python Developer"
        assert vacancies[1].name == "Java Developer"

    @patch('requests.Session.get')
    def test_get_vacancies_empty_response(self, mock_get, hh_api):
        """Тест получения вакансий при пустом ответе"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies("Python", 10)

        assert vacancies == []

    @patch('requests.Session.get')
    def test_get_vacancies_without_salary(self, mock_get, hh_api):
        """Тест получения вакансий без зарплаты"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {
                    'name': 'Python Developer',
                    'area': {'name': 'Москва'},
                    'url': 'https://hh.ru/vacancy/1',
                    'salary': None,
                    'id': '1'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies("Python", 1)

        assert len(vacancies) == 1
        assert vacancies[0].salary is None

    @patch('requests.Session.get')
    def test_get_vacancies_request_exception(self, mock_get, hh_api):
        """Тест обработки исключения при запросе"""
        mock_get.side_effect = requests.RequestException("Connection error")

        vacancies = hh_api.get_vacancies("Python", 10)

        assert vacancies == []

    @patch('requests.Session.get')
    def test_get_vacancies_key_error(self, mock_get, hh_api):
        """Тест обработки KeyError при парсинге ответа"""
        mock_response = Mock()
        mock_response.json.return_value = {'invalid': 'data'}  # Нет ключа 'items'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies("Python", 10)

        assert vacancies == []

    @patch('requests.Session.get')
    def test_get_vacancies_pagination(self, mock_get, hh_api, mock_response):
        """Тест пагинации при получении вакансий"""
        # Первая страница - 2 вакансии, вторая - 1 вакансия
        mock_response1 = Mock()
        mock_response1.json.return_value = {
            'items': [
                {
                    'name': 'Python Developer',
                    'area': {'name': 'Москва'},
                    'url': 'https://hh.ru/vacancy/1',
                    'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
                    'id': '1'
                },
                {
                    'name': 'Java Developer',
                    'area': {'name': 'Санкт-Петербург'},
                    'url': 'https://hh.ru/vacancy/2',
                    'salary': {'from': 120000, 'to': 180000, 'currency': 'RUR'},
                    'id': '2'
                }
            ]
        }
        mock_response1.raise_for_status.return_value = None

        mock_response2 = Mock()
        mock_response2.json.return_value = {
            'items': [
                {
                    'name': 'Data Scientist',
                    'area': {'name': 'Москва'},
                    'url': 'https://hh.ru/vacancy/3',
                    'salary': {'from': 150000, 'to': 200000, 'currency': 'RUR'},
                    'id': '3'
                }
            ]
        }
        mock_response2.raise_for_status.return_value = None

        mock_get.side_effect = [mock_response1, mock_response2]

        vacancies = hh_api.get_vacancies("Developer", 3)

        assert len(vacancies) == 3
        assert vacancies[0].name == "Python Developer"
        assert vacancies[1].name == "Java Developer"
        assert vacancies[2].name == "Data Scientist"