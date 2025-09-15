import pytest
from unittest.mock import Mock, patch, MagicMock
from src.user_interface import UserInterface
from src.vacancy import Vacancy


class TestUserInterface:
    @pytest.fixture
    def ui(self):
        """Фикстура для создания экземпляра UserInterface с моками"""
        with patch('src.user_interface.hh_API') as mock_hh_api, \
                patch('src.user_interface.FileHandlerJSON') as mock_file_handler:
            mock_hh_api_instance = Mock()
            mock_file_handler_instance = Mock()

            mock_hh_api.return_value = mock_hh_api_instance
            mock_file_handler.return_value = mock_file_handler_instance

            ui = UserInterface()
            ui.hh_api = mock_hh_api_instance
            ui.file_handler = mock_file_handler_instance

            yield ui

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
            )
        ]

    @patch('builtins.input')
    @patch('builtins.print')
    def test_show_menu_exit(self, mock_print, mock_input, ui):
        """Тест выхода из меню"""
        mock_input.side_effect = ['0']  # Выбор выхода

        ui.show_menu()

        mock_print.assert_any_call("До свидания!")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_show_menu_invalid_choice(self, mock_print, mock_input, ui):
        """Тест обработки неверного выбора в меню"""
        mock_input.side_effect = ['invalid', '0']  # Неверный выбор, затем выход

        ui.show_menu()

        mock_print.assert_any_call("Неверный выбор. Попробуйте снова.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_vacancies_success(self, mock_print, mock_input, ui, sample_vacancies):
        """Тест успешного поиска вакансий"""
        mock_input.side_effect = ['Python', '2']
        ui.hh_api.get_vacancies.return_value = sample_vacancies

        ui.search_vacancies()

        ui.hh_api.get_vacancies.assert_called_once_with("Python", 2)
        mock_print.assert_any_call("Найдено вакансий: 2")
        assert mock_print.call_count >= 3  # Должны быть вызовы печати

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_vacancies_empty_keyword(self, mock_print, mock_input, ui):
        """Тест поиска с пустым запросом"""
        mock_input.side_effect = ['', '2']  # Пустой запрос

        ui.search_vacancies()

        mock_print.assert_any_call("Запрос не может быть пустым!")
        ui.hh_api.get_vacancies.assert_not_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_vacancies_invalid_amount(self, mock_print, mock_input, ui):
        """Тест поиска с неверным количеством"""
        mock_input.side_effect = ['Python', 'invalid', '0']  # Неверное количество

        ui.search_vacancies()

        mock_print.assert_any_call("Пожалуйста, введите число!")
        ui.hh_api.get_vacancies.assert_not_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_vacancies_negative_amount(self, mock_print, mock_input, ui):
        """Тест поиска с отрицательным количеством"""
        mock_input.side_effect = ['Python', '-5']  # Отрицательное количество

        ui.search_vacancies()

        mock_print.assert_any_call("Количество должно быть положительным числом!")
        ui.hh_api.get_vacancies.assert_not_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_vacancies_no_results(self, mock_print, mock_input, ui):
        """Тест поиска без результатов"""
        mock_input.side_effect = ['Python', '2']
        ui.hh_api.get_vacancies.return_value = []  # Пустой результат

        ui.search_vacancies()

        mock_print.assert_any_call("Вакансии не найдены.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_show_top_vacancies_success(self, mock_print, mock_input, ui, sample_vacancies):
        """Тест показа топ вакансий"""
        mock_input.side_effect = ['2']
        ui.file_handler.get_vacancies.return_value = sample_vacancies

        ui.show_top_vacancies()

        ui.file_handler.get_vacancies.assert_called_once()
        mock_print.assert_any_call("Топ-2 вакансий по зарплате:")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_show_top_vacancies_no_salary(self, mock_print, mock_input, ui):
        """Тест показа топ вакансий без зарплаты"""
        mock_input.side_effect = ['2']
        # Вакансии без зарплаты
        vacancies_no_salary = [
            Vacancy(
                name="Python Developer",
                city="Москва",
                url="https://hh.ru/vacancy/1",
                salary=None,
                vacancy_id="1"
            )
        ]
        ui.file_handler.get_vacancies.return_value = vacancies_no_salary

        ui.show_top_vacancies()

        mock_print.assert_any_call("В файле нет вакансий с указанной зарплатой.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_show_top_vacancies_invalid_amount(self, mock_print, mock_input, ui):
        """Тест показа топ вакансий с неверным количеством"""
        mock_input.side_effect = ['invalid']  # Неверное количество

        ui.show_top_vacancies()

        mock_print.assert_any_call("Пожалуйста, введите число!")
        ui.file_handler.get_vacancies.assert_not_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_in_file_success(self, mock_print, mock_input, ui, sample_vacancies):
        """Тест поиска в файле с результатами"""
        mock_input.side_effect = ['Python']
        ui.file_handler.get_vacancies.return_value = sample_vacancies[:1]  # Только Python разработчик

        ui.search_in_file()

        ui.file_handler.get_vacancies.assert_called_once_with(name='Python')
        mock_print.assert_any_call("Найдено вакансий в файле: 1")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_in_file_empty_keyword(self, mock_print, mock_input, ui):
        """Тест поиска в файле с пустым запросом"""
        mock_input.side_effect = ['']  # Пустой запрос

        ui.search_in_file()

        mock_print.assert_any_call("Ключевое слово не может быть пустым!")
        ui.file_handler.get_vacancies.assert_not_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_in_file_no_results(self, mock_print, mock_input, ui):
        """Тест поиска в файле без результатов"""
        mock_input.side_effect = ['Python']
        ui.file_handler.get_vacancies.return_value = []  # Пустой результат

        ui.search_in_file()

        mock_print.assert_any_call("Вакансии не найдены.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_save_to_file_success(self, mock_print, mock_input, ui, sample_vacancies):
        """Тест сохранения вакансий в файл"""
        mock_input.side_effect = ['Python', '2']
        ui.hh_api.get_vacancies.return_value = sample_vacancies
        ui.file_handler.add_vacancies.return_value = 2  # Успешно добавлено 2 вакансии

        ui.save_to_file()

        ui.hh_api.get_vacancies.assert_called_once_with("Python", 2)
        ui.file_handler.add_vacancies.assert_called_once_with(sample_vacancies)
        mock_print.assert_any_call("Успешно сохранено 2 вакансий.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_save_to_file_no_results(self, mock_print, mock_input, ui):
        """Тест сохранения без результатов"""
        mock_input.side_effect = ['Python', '2']
        ui.hh_api.get_vacancies.return_value = []  # Пустой результат

        ui.save_to_file()

        mock_print.assert_any_call("Вакансии не найдены.")
        ui.file_handler.add_vacancies.assert_not_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_vacancy_success(self, mock_print, mock_input, ui):
        """Тест успешного удаления вакансии"""
        mock_input.side_effect = ['1']
        ui.file_handler.delete_vacancy.return_value = True  # Успешное удаление

        ui.delete_vacancy()

        ui.file_handler.delete_vacancy.assert_called_once_with("1")
        mock_print.assert_any_call("Вакансия успешно удалена.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_vacancy_not_found(self, mock_print, mock_input, ui):
        """Тест удаления несуществующей вакансии"""
        mock_input.side_effect = ['999']
        ui.file_handler.delete_vacancy.return_value = False  # Вакансия не найдена

        ui.delete_vacancy()

        mock_print.assert_any_call("Вакансия с таким ID не найдена.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_vacancy_empty_id(self, mock_print, mock_input, ui):
        """Тест удаления с пустым ID"""
        mock_input.side_effect = ['']  # Пустой ID

        ui.delete_vacancy()

        mock_print.assert_any_call("ID не может быть пустым!")
        ui.file_handler.delete_vacancy.assert_not_called()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_clear_vacancies_confirmed(self, mock_print, mock_input, ui):
        """Тест очистки вакансий с подтверждением"""
        mock_input.side_effect = ['y']  # Подтверждение

        ui.clear_vacancies()

        ui.file_handler.clear_all.assert_called_once()
        mock_print.assert_any_call("Все вакансии удалены.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_clear_vacancies_cancelled(self, mock_print, mock_input, ui):
        """Тест отмены очистки вакансий"""
        mock_input.side_effect = ['n']  # Отмена

        ui.clear_vacancies()

        ui.file_handler.clear_all.assert_not_called()
        mock_print.assert_any_call("Операция отменена.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_show_all_vacancies_with_data(self, mock_print, mock_input, ui, sample_vacancies):
        """Тест показа всех вакансий с данными"""
        ui.file_handler.get_vacancies.return_value = sample_vacancies

        ui.show_all_vacancies()

        ui.file_handler.get_vacancies.assert_called_once()
        mock_print.assert_any_call("Всего вакансий в файле: 2")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_show_all_vacancies_empty(self, mock_print, mock_input, ui):
        """Тест показа всех вакансий без данных"""
        ui.file_handler.get_vacancies.return_value = []  # Пустой файл

        ui.show_all_vacancies()

        mock_print.assert_any_call("В файле нет вакансий.")