from src.user_interface import UserInterface

def main():
    """Главная функция программы"""
    print("Добро пожаловать в систему поиска вакансий!")
    ui = UserInterface()
    ui.show_menu()

if __name__ == "__main__":
    main()