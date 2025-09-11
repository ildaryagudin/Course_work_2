import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from src.hh_api import hh_API, JobAPI  # замените your_module на имя вашего модуля


class TestJobAPI:
    """Тесты для абстрактного класса JobAPI"""

    def test_abc_class_cannot_be_instantiated(self):
        """Тест, что абстрактный класс нельзя инстанцировать"""
        with pytest.raises(TypeError):
            JobAPI()


class TestHHAPI:
    """Тесты для класса hh_API"""

    @pytest.fixture
    def hh_api(self):
        """Фикстура для создания экземпляра hh_API"""
        return hh_API()

    @pytest.fixture
    def mock_vacancies_response(self):
        """Фикстура для мок-ответа с вакансиями"""
        return {
            'items': [
                {
                    'name': 'Python Developer',
                    'area': {'name': 'Москва'},
                    'url': 'https://hh.ru/vacancy/123',
                    'salary': {'from': 100000, 'to': 150000, 'currency': 'RUB'},
                    'id': '123'
                },
                {
                    'name': 'Data Scientist',
                    'area': {'name': 'Санкт-Петербург'},
                    'url': 'https://hh.ru/vacancy/456',
                    'salary': None,
                    'id': '456'
                }
            ]
        }

    def test_hh_api_inherits_from_job_api(self):
        """Тест, что hh_API наследуется от JobAPI"""
        assert issubclass(hh_API, JobAPI)

    def test_hh_api_can_be_instantiated(self):
        """Тест, что hh_API можно инстанцировать"""
        api = hh_API()
        assert isinstance(api, hh_API)
        assert api._hh_API__session is None

    @patch('your_module.requests.Session')  # замените your_module
    def test_connect_method(self, mock_session_class, hh_api):
        """Тест метода _connect"""
        # Настройка моков
        mock_session = Mock()
        mock_response = Mock()
        mock_session_class.return_value = mock_session
        mock_session.get.return_value = mock_response
        mock_response.raise_for_status.return_value = None

        # Вызов метода
        result = hh_api._connect()

        # Проверки
        mock_session_class.assert_called_once()
        mock_session.get.assert_called_once_with('https://api.hh.ru/vacancies')
        mock_response.raise_for_status.assert_called_once()
        assert result == mock_response
        assert hh_api._hh_API__session == mock_session

    @patch('your_module.requests.Session')  # замените your_module
    def test_connect_method_raises_exception_on_error(self, mock_session_class, hh_api):
        """Тест, что _connect выбрасывает исключение при ошибке"""
        mock_session = Mock()
        mock_response = Mock()
        mock_session_class.return_value = mock_session
        mock_session.get.return_value = mock_response
        mock_response.raise_for_status.side_effect = requests.RequestException("Connection error")

        with pytest.raises(requests.RequestException):
            hh_api._connect()

    @patch.object(hh_API, '_connect')
    def test_load_vacancies_success(self, mock_connect, hh_api, mock_vacancies_response):
        """Тест успешной загрузки вакансий"""
        # Настройка моков
        mock_session = Mock()
        mock_response = Mock()
        hh_api._hh_API__session = mock_session
        mock_session.get.return_value = mock_response
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_vacancies_response

        # Вызов метода
        keyword = "Python"
        per_page = 10
        page = 0
        result = hh_api.load_vacancies(keyword, per_page, page)

        # Проверки
        mock_connect.assert_called_once()
        mock_session.get.assert_called_once_with(
            'https://api.hh.ru/vacancies',
            params={'text': keyword, 'per_page': per_page, 'page': page}
        )
        mock_response.raise_for_status.assert_called_once()

        # Проверка структуры результата
        assert len(result) == 2
        assert result[0]['name'] == 'Python Developer'
        assert result[0]['city'] == 'Москва'
        assert result[0]['url'] == 'https://hh.ru/vacancy/123'
        assert result[0]['salary'] == {'from': 100000, 'to': 150000, 'currency': 'RUB'}
        assert result[0]['id'] == '123'

        # Проверка обработки None salary
        assert result[1]['salary'] is None

    @patch.object(hh_API, '_connect')
    def test_load_vacancies_empty_response(self, mock_connect, hh_api):
        """Тест загрузки вакансий с пустым ответом"""
        mock_session = Mock()
        mock_response = Mock()
        hh_api._hh_API__session = mock_session
        mock_session.get.return_value = mock_response
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'items': []}

        result = hh_api.load_vacancies("NonExistentKeyword", 10, 0)

        assert result == []

    @patch.object(hh_API, '_connect')
    def test_load_vacancies_request_exception(self, mock_connect, hh_api):
        """Тест обработки исключения при запросе вакансий"""
        mock_session = Mock()
        mock_response = Mock()
        hh_api._hh_API__session = mock_session
        mock_session.get.return_value = mock_response
        mock_response.raise_for_status.side_effect = requests.RequestException("API error")

        with pytest.raises(requests.RequestException):
            hh_api.load_vacancies("Python", 10, 0)

    def test_load_vacancies_without_connection(self, hh_api):
        """Тест, что load_vacancies вызывает _connect если сессия не установлена"""
        assert hh_api._hh_API__session is None

        with patch.object(hh_api, '_connect') as mock_connect, \
                patch.object(hh_api, '_hh_API__session') as mock_session:
            mock_response = Mock()
            mock_session.get.return_value = mock_response
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {'items': []}

            hh_api.load_vacancies("test", 10, 0)

            mock_connect.assert_called_once()

    @pytest.mark.parametrize("per_page,page", [
        (10, 0),
        (20, 1),
        (50, 2),
        (100, 5)
    ])
    @patch.object(hh_API, '_connect')
    def test_load_vacancies_with_different_parameters(self, mock_connect, hh_api, per_page, page):
        """Параметризованный тест с разными параметрами per_page и page"""
        mock_session = Mock()
        mock_response = Mock()
        hh_api._hh_API__session = mock_session
        mock_session.get.return_value = mock_response
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'items': []}

        keyword = "Python"
        hh_api.load_vacancies(keyword, per_page, page)

        mock_session.get.assert_called_once_with(
            'https://api.hh.ru/vacancies',
            params={'text': keyword, 'per_page': per_page, 'page': page}
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])