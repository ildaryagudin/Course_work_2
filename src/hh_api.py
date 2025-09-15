import requests
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str, amount: int):
        pass


class hh_API(JobAPI):
    BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.session = requests.Session()

    def get_vacancies(self, keyword: str, amount: int):
        """Получение вакансий по ключевому слову"""
        vacancies = []
        page = 0
        per_page = min(100, amount)

        while len(vacancies) < amount:
            try:
                page_vacancies = self._load_page(keyword, page, per_page)
                if not page_vacancies:
                    break

                vacancies.extend(page_vacancies)
                page += 1

                # Если на странице меньше вакансий, чем запрошено, выходим
                if len(page_vacancies) < per_page:
                    break

            except Exception as e:
                print(f"Ошибка при загрузке страницы {page}: {e}")
                break

        return vacancies[:amount]

    def _load_page(self, keyword: str, page: int, per_page: int):
        """Загрузка одной страницы вакансий"""
        params = {
            'text': keyword,
            'per_page': per_page,
            'page': page,
            'only_with_salary': True
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return [
                Vacancy(
                    name=vacancy['name'],
                    city=vacancy['area']['name'],
                    url=vacancy['url'],
                    salary=vacancy['salary'],
                    vacancy_id=vacancy['id']
                )
                for vacancy in data.get('items', [])
            ]

        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []
        except KeyError as e:
            print(f"Ошибка обработки данных: {e}")
            return []