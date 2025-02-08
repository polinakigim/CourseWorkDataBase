import psycopg2

from src.abstract_classes import DBManagerABC


class DBManager(DBManagerABC):

    def __init__(self, params_db: dict, db_name: str):
        self.avg_salary = None
        self.params_db = params_db
        self.db_name = db_name

    def get_companies_and_vacancies_count(self):
        """Метод для получения всех компаний и количество вакансий у каждой компании"""
        conn = psycopg2.connect(**self.params_db)

        with conn.cursor() as cur:
            cur.execute(
                """
            SELECT company_name, COUNT(vacancies.company_id) FROM companies
            INNER JOIN vacancies ON companies.company_id=vacancies.company_id
            GROUP BY company_name
            """
            )
            result = cur.fetchall()

        conn.close()
        return result

    def get_all_vacancies(self):
        """Метод получения всех вакансий с указанием: название компании, название вакансии, зарплата, ссылка на вакансию"""
        conn = psycopg2.connect(**self.params_db)
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT company_name, vacancy_name, salary_from, salary_to, url
                    FROM companies
                    RIGHT JOIN vacancies USING(company_id)
                    """
            )
            result = cur.fetchall()

        conn.close()
        return result

    def get_avg_salary(self):
        """Метод получения средней зарплаты по вакансиям"""
        conn = psycopg2.connect(**self.params_db)

        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies""")
            result = cur.fetchall()

        conn.close()
        average = str(result[0]).split("'")[1]

        self.avg_salary = float(average[0:8])

        return f"{self.avg_salary}"

    def get_vacancies_with_higher_salary(self):
        """Метод получения выше средней зарплаты по всем вакансиям"""
        conn = psycopg2.connect(**self.params_db)

        with conn.cursor() as cur:
            cur.execute(
                """
                 SELECT vacancy_name, salary_from, salary_to, url 
                 FROM vacancies
                 WHERE salary_to >= (SELECT AVG(salary_to) 
                 FROM vacancies)
                """
            )
            result = cur.fetchall()

        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Метод получения списка всех вакансий в названии которых есть ключевые слова"""
        key_word = keyword.title()
        conn = psycopg2.connect(**self.params_db)

        with conn.cursor() as cur:
            cur.execute(
                f"""SELECT * FROM vacancies WHERE vacancy_name LIKE '%{key_word}%'"""
            )
            result = cur.fetchall()

        conn.close()

        return result
