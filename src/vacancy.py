class Vacancy:
    def __init__(self, name, city, url, salary, vacancy_id):
        self.name = name
        self.city = city
        self.url = url
        self.salary = salary
        self.id = vacancy_id

    def __str__(self):
        salary_str = self._format_salary()
        return f"""
Название: {self.name}
Город: {self.city}
Зарплата: {salary_str}
Ссылка: {self.url}
ID: {self.id}
------------------------
"""

    def _format_salary(self):
        if not self.salary:
            return "Зарплата не указана"

        salary_from = self.salary.get('from', 'Не указано')
        salary_to = self.salary.get('to', 'Не указано')
        currency = self.salary.get('currency', '')

        if salary_from and salary_to:
            return f"{salary_from} - {salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        else:
            return "Зарплата не указана"

    def to_dict(self):
        return {
            'name': self.name,
            'city': self.city,
            'url': self.url,
            'salary': self.salary,
            'id': self.id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name'),
            city=data.get('city'),
            url=data.get('url'),
            salary=data.get('salary'),
            vacancy_id=data.get('id')
        )