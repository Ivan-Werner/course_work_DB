from decimal import Decimal

import psycopg2


class DBManager:
    """Класс для работы с БД"""
    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='db_headhunter', **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute("""SELECT employer_name, COUNT(vacancies.employer_id)
                            FROM employers
                            JOIN vacancies USING (employer_id)
                            GROUP BY employer_name""")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute("""SELECT employer_name, vacancy_name, salary, vacancy_url
                            FROM vacancies
                            JOIN employers USING (employer_id)
                            WHERE salary != 0 AND salary IS NOT NULL""")
        return self.cur.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        self.cur.execute("""SELECT AVG(salary) FROM vacancies""")
        result = self.cur.fetchone()
        avg_salary = Decimal(result[0])
        return round(avg_salary)

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.cur.execute("""SELECT vacancy_name, salary
                            FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)""")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        keyword = f"%{keyword.lower()}%"
        self.cur.execute("""SELECT vacancy_name FROM vacancies WHERE vacancy_name LIKE %s""", (keyword,))
        return self.cur.fetchall()
