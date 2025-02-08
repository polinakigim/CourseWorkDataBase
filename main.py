from src.config import config
from src.db_manager import DBManager
from src.utils import create_database, save_data_to_database


def main():
    params = config()

    create_database()
    save_data_to_database()

    db_company = DBManager(params, "test")

    print(
        "\nДобро пожаловать в систему! Пожалуйста, выберите одно из следующих действий:"
    )

    menu = """
    1. Получить количество вакансий по каждой компании
    2. Получить все вакансии по каждой компании
    3. Получить среднюю зарплату по всем компаниям
    4. Вывести вакансии, у которых зарплата выше средней по всем компаниям
    5. Вывести вакансии по ключевому слову в названии вакансии
    """
    print(menu)

    user_choice = input("Ваш выбор (1-5): ")

    if user_choice == "1":
        result = db_company.get_companies_and_vacancies_count()
        print("\nКоличество вакансий по каждой компании:")
        for company, vacancy_count in result:
            print(f"{company} - {vacancy_count} вакансий.")

    elif user_choice == "2":
        result = db_company.get_all_vacancies()
        print("\nВсе вакансии по компаниям:")
        for company, vacancy, min_salary, max_salary, link in result:
            print(f"Компания: {company}")
            print(f"Вакансия: {vacancy}")
            print(f"Зарплата: от {min_salary} до {max_salary} руб.")
            print(f"Ссылка: {link}")
            print("-" * 40)

    elif user_choice == "3":
        avg_salary = db_company.get_avg_salary()
        print(f"\nСредняя зарплата по всем компаниям: {avg_salary} руб.")

    elif user_choice == "4":
        result = db_company.get_vacancies_with_higher_salary()
        print("\nВакансии с зарплатой выше средней по всем компаниям:")
        for company, min_salary, max_salary, link in result:
            print(f"Компания: {company}")
            print(f"Зарплата: от {min_salary} до {max_salary} руб.")
            print(f"Ссылка: {link}")
            print("-" * 40)

    elif user_choice == "5":
        keyword = input("Введите ключевое слово для поиска вакансий:\n").title()
        result = db_company.get_vacancies_with_keyword(keyword)
        if result:
            print(f"\nВакансии, содержащие ключевое слово '{keyword}':")
            for res in result:
                print(res)
        else:
            print(f"\nВакансии с ключевым словом '{keyword}' не найдены.")

    else:
        print("\nНекорректный ввод. Пожалуйста, выберите вариант от 1 до 5.")


if __name__ == "__main__":
    main()
