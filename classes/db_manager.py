from config import config
import psycopg2


class DBManager():
    @staticmethod
    def get_companies_and_vacancies_count(params):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        и выводит их на печать
        """
        try:
            with psycopg2.connect(**params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT companies.company_name, COUNT(*) FROM companies
                        JOIN vacancies USING (company_id)
                        GROUP BY company_name
                        ORDER BY COUNT(*) DESC
                    """)
                    result = cur.fetchall()

                user_answer = input('Желаете вывести список всех компаний и количество вакансий у каждой компании '
                                    'на печать: 1 - да; любая клавиша для выхода: ')
                if user_answer == '1':
                    for company in result:
                        print(f'Компания {company[0]} - {company[1]} вакансий')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def get_all_vacancies(params):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        try:
            with psycopg2.connect(**params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT companies.company_name, vacancy_name, 
                        (salary_from + salary_to)/2 AS average_salary, vacancy_url FROM vacancies
                        JOIN companies USING (company_id)
                        ORDER BY company_name
                    """)
                    result = cur.fetchall()

                user_answer = input(
                    'Желаете вывести список всех вакансий на печать: 1 - да; любая клавиша для выхода: ')
                if user_answer == '1':
                    for vacancy in result:
                        print(*vacancy, sep=' / ')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def get_avg_salary(params):
        """
        Получает среднюю зарплату по вакансиям
        """
        try:
            with psycopg2.connect(**params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT CAST(AVG(salary_from + salary_to)/2 AS INT) FROM vacancies
                    """)
                    result = cur.fetchone()[0]

                user_answer = input('Желаете вывести среднюю зарплату по вакансиям на печать: 1 - да; любая клавиша '
                                    'для выхода: ')
                if user_answer == '1':
                    print(f'Средняя зарплата: {result} руб.')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def get_vacancies_with_higher_salary(params):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        try:
            with psycopg2.connect(**params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT * FROM vacancies
                        WHERE (salary_from + salary_to)/2 > (SELECT AVG(salary_from + salary_to)/2 FROM vacancies)
                        ORDER BY salary_from DESC
                    """)
                    result = cur.fetchall()

                user_answer = input(
                    'Желаете вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям на '
                    'печать: 1 - да; любая клавиша для выхода: ')
                if user_answer == '1':
                    for vacancy in result:
                        print(*vacancy, sep=' / ')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def get_vacancies_with_keyword(params):
        """
        Получает список вакансий с указанием ключевого слова
        """
        user_keyword = input('Введите ключевое слово для поиска вакансий: ')
        if user_keyword:
            try:
                with psycopg2.connect(**params) as conn:
                    conn.autocommit = True
                    with conn.cursor() as cur:
                        cur.execute(f"""
                            SELECT * FROM vacancies
                            WHERE vacancy_name LIKE '%{user_keyword}%'
                            ORDER BY salary_from
                        """)
                        result = cur.fetchall()
                        if result:
                            user_answer = input(
                                'Желаете вывести список всех вакансий, отобранных по ключевому слову на '
                                'печать: 1 - да; любая клавиша для выхода: ')
                            if user_answer == '1':
                                for vacancy in result:
                                    print(*vacancy, sep=' / ')
                        else:
                            print('По Вашему запросу ничего не нашлось')
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        print('Программа завершена')
