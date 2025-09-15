import pytest
from unittest.mock import patch, MagicMock
from main import main


class TestMain:
    @patch('src.main.UserInterface')
    @patch('builtins.print')
    def test_main_function(self, mock_print, mock_user_interface):
        """Тест главной функции"""
        # Создаем мок для экземпляра UserInterface
        mock_ui_instance = MagicMock()
        mock_user_interface.return_value = mock_ui_instance

        # Запускаем главную функцию
        main()

        # Проверяем, что был создан экземпляр и вызван show_menu
        mock_user_interface.assert_called_once()
        mock_ui_instance.show_menu.assert_called_once()
        mock_print.assert_any_call("Добро пожаловать в систему поиска вакансий!")