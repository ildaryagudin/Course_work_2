from src.hh_api import hh_API
from src.file_handler import FileHandlerJSON

from pprint import pprint

def user_interaction():
    hh_api = hh_API
    file_handler = FileHandlerJSON()

    while True:
        print("\nВыберите действие")
        print("1. Поиск вакансий по ключевому слову")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом из файла")
        print("100. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            keyword = input("Введите поисковый запрос: ")
            amount = input("Введите кол-во вакансий для получения: ")

            try:
                vacancies = hh_api.load_vacancies(keyword, amount)
                print(vacancies)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        elif choice == '2':
            n = int(input("Введите кол-во вакансий для получения: "))
            vacancies = file_handler.get_vacancies()

            remove_without_salary = [vacan for vacan in vacancies if vacan['salary'] == 'Зарплата не указана']
            sorted_vacancies = sorted(remove_without_salary, key=lambda x: x.get('salary', 0), reverse=True)[:n]

            if sorted_vacancies:
                for vacancy in sorted_vacancies:
                    print(f"""
                                Название: {vacancy['name']},
                                Город: {vacancy.get('area', None)},
                                Зарплата: {vacancy['salary']},
                                Ссылка: {vacancy['url']}
                            """
                    )
            else:
                print("Вакансии не найдены")

        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска в файле: ")
            vacancies = file_handler.get_vacancies(name=keyword)
            if vacancies:
                for vacancy in vacancies:
                    print(f"""
                                Название: {vacancy['name']},
                                Город: {vacancy.get('area', None)},
                                Зарплата: {vacancy['salary']},
                                Ссылка: {vacancy['url']}
                            """
                    )
            else:
                print("Вакансии не найдены")

        elif choice == '100':
            print("Выход из программы")
            break



if __name__ == "__main__":
    user_interaction()
