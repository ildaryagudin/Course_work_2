from src.hh_api import hh_API
from src.file_handler import FileHandlerJSON


def user_interaction():
    hh_api = hh_API()  # Исправлено: добавлены скобки для создания экземпляра
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
                # Исправлено: передаем все три параметра
                vacancies = hh_api.load_vacancies(keyword, per_page=int(amount), page=0)
                print(f"Найдено вакансий: {len(vacancies)}")
                for vacancy in vacancies:
                    print(f"""
Название: {vacancy['name']},
Город: {vacancy['city']},
Зарплата: {vacancy['salary']},
Ссылка: {vacancy['url']}
ID: {vacancy['id']}
------------------------
""")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '2':
            n = int(input("Введите кол-во вакансий для получения: "))
            vacancies = file_handler.get_vacancies()

            # Исправлено: правильная фильтрация по зарплате
            remove_without_salary = [vacan for vacan in vacancies if vacan.get('salary') is not None]
            sorted_vacancies = sorted(remove_without_salary,
                                      key=lambda x: x.get('salary', {}).get('from', 0) if isinstance(x.get('salary'),
                                                                                                     dict) else 0,
                                      reverse=True)[:n]

            if sorted_vacancies:
                for vacancy in sorted_vacancies:
                    salary = vacancy.get('salary', {})
                    if salary:
                        salary_str = f"{salary.get('from', 'Не указано')} - {salary.get('to', 'Не указано')} {salary.get('currency', '')}"
                    else:
                        salary_str = "Зарплата не указана"

                    print(f"""
Название: {vacancy['name']},
Город: {vacancy.get('city', 'Не указан')},
Зарплата: {salary_str},
Ссылка: {vacancy['url']}
------------------------
""")
            else:
                print("Вакансии не найдены")

        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска в файле: ")
            vacancies = file_handler.get_vacancies()
            # Фильтруем вакансии по ключевому слову
            filtered_vacancies = [v for v in vacancies if keyword.lower() in v['name'].lower()]

            if filtered_vacancies:
                for vacancy in filtered_vacancies:
                    salary = vacancy.get('salary', {})
                    if salary:
                        salary_str = f"{salary.get('from', 'Не указано')} - {salary.get('to', 'Не указано')} {salary.get('currency', '')}"
                    else:
                        salary_str = "Зарплата не указана"

                    print(f"""
Название: {vacancy['name']},
Город: {vacancy.get('city', 'Не указан')},
Зарплата: {salary_str},
Ссылка: {vacancy['url']}
------------------------
""")
            else:
                print("Вакансии не найдены")

        elif choice == '100':
            print("Выход из программы")
            break


if __name__ == "__main__":
    user_interaction()