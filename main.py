from src.hh_api import HeadHunterAPI
from src.config import config
from src.db_work import DBManager
from src.utils import create_database, insert_tables_to_database


def main():
    """Функция для работы с программой"""
    params = config()

    data_employer = HeadHunterAPI().get_employers()
    data_vacancies = HeadHunterAPI().load_vacancies()
    create_database('db_headhunter', params)
    insert_tables_to_database(data_employer, data_vacancies, 'db_headhunter', params)
    db_manager = DBManager(params)

    message = ("""
        Введите цифру для получения нужной Вам информации    
        1 - Получить список всех компаний и количество вакансий у каждой компаний.
        2 - Получить список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        3 - Получить среднюю зарплату по вакансиям.
        4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        5 - Получить список всех вакансий, в названии которых содержатся переданные в метод слова.
        0 - Завершить программу\n
    """)
    print(message)
    while True:
        user_input = input()
        if user_input == "1":
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компаний:")
            for i in companies_and_vacancies_count:
                print(i)
            print(message)
            print("Введите соответствующую цифру для вывода информации")
        elif user_input == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print("Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию:")
            for i in all_vacancies:
                print(i)
            print(message)
            print("Введите соответствующую цифру для вывода информации")
        elif user_input == '3':
            avg_salary = db_manager.get_avg_salary()
            print("Средняя зарплата по вакансиям:")
            print(avg_salary)
            print(message)
            print("Введите соответствующую цифру для вывода информации")
        elif user_input == "4":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print("Список всех вакансий, у которых зарплата выше средней по всем вакансиям:")
            for i in vacancies_with_higher_salary:
                print(i)
            print(message)
            print("Введите соответствующую цифру для вывода информации")
        elif user_input == "5":
            user_word = input("Введите ключ слово\n").lower()
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_word)
            print("Список всех вакансий, в названии которых содержатся переданные в метод слова:")
            for i in vacancies_with_keyword:
                print(i)
            print(message)
            print("Введите соответствующую цифру для вывода информации")
        elif user_input == "0":
            print("Завершение работы.")
            break


if __name__ == '__main__':
    main()