import abc
import requests


class JobAPI(abc.ABC):
    @abc.abstractmethod
    def _connect(self):
        """Метод для подключения к API"""
        pass

    @abc.abstractmethod
    def get_vacancies(self, keyword: str, page:int):
        """Метод для получения вакансий по ключевому слову"""
        pass



class hh_API(JobAPI):
    BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.__session = None

    def _connect(self):
        """Метод для подключения к API"""
        self.__session = requests.Session()
        response = self.__session.get(self.BASE_URL)
        response.raise_for_status()
        return response

    def get_vacancies(self, keyword: str, page: int):
        """Реализация абстрактного метода"""
        return self.load_vacancies(keyword, per_page=100, page=page)

    def load_vacancies(self, keyword: str, per_page: int, page: int):
        """Метод для получения вакансий по ключевому слову"""
        self._connect()

        params = {
            'text': keyword,
            'per_page': per_page,
            'page': page
        }

        response = self.__session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        vacancies = response.json().get('items', [])

        return [
            {
                'name': vacancy['name'],
                'city': vacancy['area']['name'],
                'url': vacancy['url'],
                "salary": vacancy['salary'],
                'id': vacancy['id']
            }
            for vacancy in vacancies
        ]




