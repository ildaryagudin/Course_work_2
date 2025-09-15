import pytest
from src.vacancy import Vacancy


class TestVacancy:
    def test_vacancy_creation(self):
        """Тест создания вакансии"""
        vacancy = Vacancy(
            name="Python Developer",
            city="Москва",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            vacancy_id="123"
        )

        assert vacancy.name == "Python Developer"
        assert vacancy.city == "Москва"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary == {"from": 100000, "to": 150000, "currency": "RUR"}
        assert vacancy.id == "123"

    def test_vacancy_without_salary(self):
        """Тест создания вакансии без зарплаты"""
        vacancy = Vacancy(
            name="Python Developer",
            city="Москва",
            url="https://hh.ru/vacancy/123",
            salary=None,
            vacancy_id="123"
        )

        assert vacancy.salary is None

    def test_format_salary_with_full_info(self):
        """Тест форматирования зарплаты с полной информацией"""
        vacancy = Vacancy(
            name="Test",
            city="Test",
            url="test",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            vacancy_id="123"
        )

        assert vacancy._format_salary() == "100000 - 150000 RUR"

    def test_format_salary_only_from(self):
        """Тест форматирования зарплаты только с нижней границей"""
        vacancy = Vacancy(
            name="Test",
            city="Test",
            url="test",
            salary={"from": 100000, "currency": "RUR"},
            vacancy_id="123"
        )

        assert vacancy._format_salary() == "от 100000 RUR"

    def test_format_salary_only_to(self):
        """Тест форматирования зарплаты только с верхней границей"""
        vacancy = Vacancy(
            name="Test",
            city="Test",
            url="test",
            salary={"to": 150000, "currency": "RUR"},
            vacancy_id="123"
        )

        assert vacancy._format_salary() == "до 150000 RUR"

    def test_format_salary_none(self):
        """Тест форматирования зарплаты когда зарплата не указана"""
        vacancy = Vacancy(
            name="Test",
            city="Test",
            url="test",
            salary=None,
            vacancy_id="123"
        )

        assert vacancy._format_salary() == "Зарплата не указана"

    def test_to_dict(self):
        """Тест преобразования вакансии в словарь"""
        vacancy = Vacancy(
            name="Python Developer",
            city="Москва",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            vacancy_id="123"
        )

        result = vacancy.to_dict()

        expected = {
            'name': 'Python Developer',
            'city': 'Москва',
            'url': 'https://hh.ru/vacancy/123',
            'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
            'id': '123'
        }

        assert result == expected

    def test_from_dict(self):
        """Тест создания вакансии из словаря"""
        data = {
            'name': 'Python Developer',
            'city': 'Москва',
            'url': 'https://hh.ru/vacancy/123',
            'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
            'id': '123'
        }

        vacancy = Vacancy.from_dict(data)

        assert vacancy.name == "Python Developer"
        assert vacancy.city == "Москва"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary == {'from': 100000, 'to': 150000, 'currency': 'RUR'}
        assert vacancy.id == "123"

    def test_str_representation(self):
        """Тест строкового представления вакансии"""
        vacancy = Vacancy(
            name="Python Developer",
            city="Москва",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            vacancy_id="123"
        )

        result = str(vacancy)

        assert "Python Developer" in result
        assert "Москва" in result
        assert "100000 - 150000 RUR" in result
        assert "https://hh.ru/vacancy/123" in result
        assert "123" in result