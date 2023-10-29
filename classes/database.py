import psycopg2
import json
from config import PATH_TO_COMPANIES_JSON, PATH_TO_VACANCIES_JSON


class Database:
    def __init__(self):
        """
        Инициализатор экземпляров класса для работы с базой данных
        database_name: название базы данных
        params: словарь с параметрами
        """
        self.db_name = 'hh_vacancies'

    def create_database(self, params) -> None:
        """Создает новую базу данных."""

        try:
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
                cur.execute(f'CREATE DATABASE {self.db_name}')

                print(f'База данных {self.db_name} создана')
                cur.close()
                conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_tables(self, params) -> None:
        """Создает таблицы в базе данных"""
        try:
            # Обновляем имя базы данных
            params.update({'dbname': self.db_name})
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("""
                   CREATE TABLE IF NOT EXISTS companies(
                   company_id SERIAL PRIMARY KEY,
                   company_name varchar(64)
                   )""")

                cur.execute("""
                   CREATE TABLE IF NOT EXISTS vacancies(
                   vacancy_id SERIAL PRIMARY KEY,
                   company_id int REFERENCES companies(company_id) ON DELETE CASCADE,
                   vacancy_name varchar(200),
                   vacancy_city varchar(50),
                   salary_from int,
                   salary_to int,
                   currency varchar(15),
                   vacancy_url varchar(300)
                   )""")
                print('Таблицы успешно созданы')
                cur.close()
            conn.commit()
            conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_data_to_tables(self, params) -> None:
        """
        Добавляет данные в таблицы
        """
        try:
            params.update({'dbname': self.db_name})
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            with conn.cursor() as cur:
                companies = self.get_companies_from_json(PATH_TO_COMPANIES_JSON)
                vacancies = self.get_vacancies_from_json(PATH_TO_VACANCIES_JSON)

                for company in companies:
                    cur.execute(
                        f"INSERT INTO companies(company_id, company_name) VALUES (%s, %s)",
                        (company['company_HH_id'], company['company_name'])
                    )

                for vacancy in vacancies:
                    cur.execute(
                        f"INSERT INTO vacancies(vacancy_name, company_id, vacancy_city, salary_from, salary_to, "
                        f"currency, vacancy_url) "
                        f"VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            vacancy['vacancy_name'],
                            vacancy['company_id'],
                            vacancy['vacancy_city'],
                            vacancy['salary_from'],
                            vacancy['salary_to'],
                            vacancy['currency'],
                            vacancy['vacancy_url']
                        )
                    )
                print('Данные успешно добавлены')
            conn.commit()
            conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def get_companies_from_json(file_path):
        """
        Получает список компаний из json-файла
        :param file_path: путь к json-файлу
        :return: список компаний
        """
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def get_vacancies_from_json(file_path):
        """
        Получает список вакансий из json-файла
        :param file_path: путь к json-файлу
        :return: список вакансий
        """
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
