from src.hh_api import hh_API
from src.file_handler import FileHandlerJSON
from src.vacancy import Vacancy


class UserInterface:
    def __init__(self):
        self.hh_api = hh_API()
        self.file_handler = FileHandlerJSON()

    def show_menu(self):
        """Отображение главного меню"""
        while True:
            print("\n" + "=" * 50)
            print("ПЛАТФОРМА ДЛЯ ПОИСКА ВАКАНСИЙ")
            print("=" * 50)
            print("1. Поиск вакансий по ключевому слову")
            print("2. Показать топ N вакансий по зарплате")
            print("3. Поиск вакансий в файле по ключевому слову")
            print("4. Сохранить вакансии в файл")
            print("5. Удалить вакансию из файла")
            print("6. Очистить все вакансии в файле")
            print("7. Показать все вакансии в файле")
            print("0. Выход")
            print("=" * 50)

            choice = input("Выберите действие: ").strip()

            if choice == '1':
                self.search_vacancies()
            elif choice == '2':
                self.show_top_vacancies()
            elif choice == '3':
                self.search_in_file()
            elif choice == '4':
                self.save_to_file()
            elif choice == '5':
                self.delete_vacancy()
            elif choice == '6':
                self.clear_vacancies()
            elif choice == '7':
                self.show_all_vacancies()
            elif choice == '0':
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def search_vacancies(self):
        """Поиск вакансий через API"""
        keyword = input("Введите поисковый запрос: ").strip()
        if not keyword:
            print("Запрос не может быть пустым!")
            return

        try:
            amount = int(input("Введите количество вакансий для получения: ").strip())
            if amount <= 0:
                print("Количество должно быть положительным числом!")
                return
        except ValueError:
            print("Пожалуйста, введите число!")
            return

        print(f"\nПоиск вакансий по запросу '{keyword}'...")
        vacancies = self.hh_api.get_vacancies(keyword, amount)

        if vacancies:
            print(f"\nНайдено вакансий: {len(vacancies)}")
            for vacancy in vacancies:
                print(vacancy)
        else:
            print("Вакансии не найдены.")

    def show_top_vacancies(self):
        """Показать топ вакансий по зарплате"""
        try:
            n = int(input("Введите количество вакансий для отображения: ").strip())
            if n <= 0:
                print("Количество должно быть положительным числом!")
                return
        except ValueError:
            print("Пожалуйста, введите число!")
            return

        vacancies = self.file_handler.get_vacancies()

        # Фильтруем вакансии с указанной зарплатой
        vacancies_with_salary = [
            vac for vac in vacancies
            if vac.salary and vac.salary.get('from') is not None
        ]

        if not vacancies_with_salary:
            print("В файле нет вакансий с указанной зарплатой.")
            return

        # Сортируем по зарплате (от большей к меньшей)
        sorted_vacancies = sorted(
            vacancies_with_salary,
            key=lambda x: x.salary.get('from', 0) or 0,
            reverse=True
        )[:n]

        print(f"\nТоп-{n} вакансий по зарплате:")
        for i, vacancy in enumerate(sorted_vacancies, 1):
            print(f"{i}. {vacancy}")

    def search_in_file(self):
        """Поиск вакансий в файле"""
        keyword = input("Введите ключевое слово для поиска: ").strip()
        if not keyword:
            print("Ключевое слово не может быть пустым!")
            return

        vacancies = self.file_handler.get_vacancies(name=keyword)

        if vacancies:
            print(f"\nНайдено вакансий в файле: {len(vacancies)}")
            for vacancy in vacancies:
                print(vacancy)
        else:
            print("Вакансии не найдены.")

    def save_to_file(self):
        """Сохранение вакансий в файл"""
        keyword = input("Введите поисковый запрос для сохранения: ").strip()
        if not keyword:
            print("Запрос не может быть пустым!")
            return

        try:
            amount = int(input("Введите количество вакансий для сохранения: ").strip())
            if amount <= 0:
                print("Количество должно быть положительным числом!")
                return
        except ValueError:
            print("Пожалуйста, введите число!")
            return

        print(f"\nПоиск и сохранение вакансий...")
        vacancies = self.hh_api.get_vacancies(keyword, amount)

        if vacancies:
            added_count = self.file_handler.add_vacancies(vacancies)
            print(f"Успешно сохранено {added_count} вакансий.")
        else:
            print("Вакансии не найдены.")

    def delete_vacancy(self):
        """Удаление вакансии из файла"""
        vacancy_id = input("Введите ID вакансии для удаления: ").strip()
        if not vacancy_id:
            print("ID не может быть пустым!")
            return

        if self.file_handler.delete_vacancy(vacancy_id):
            print("Вакансия успешно удалена.")
        else:
            print("Вакансия с таким ID не найдена.")

    def clear_vacancies(self):
        """Очистка всех вакансий"""
        confirm = input("Вы уверены, что хотите очистить все вакансии? (y/n): ").strip().lower()
        if confirm == 'y':
            self.file_handler.clear_all()
            print("Все вакансии удалены.")
        else:
            print("Операция отменена.")

    def show_all_vacancies(self):
        """Показать все вакансии в файле"""
        vacancies = self.file_handler.get_vacancies()

        if vacancies:
            print(f"\nВсего вакансий в файле: {len(vacancies)}")
            for vacancy in vacancies:
                print(vacancy)
        else:
            print("В файле нет вакансий.")