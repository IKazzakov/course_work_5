from classes.hh_api import HeadHunterAPI
from classes.database import Database
from classes.db_manager import DBManager
from config import config

if __name__ == '__main__':
    params = config()

    hh_api = HeadHunterAPI()
    hh_api.get_vacancies_by_api()

    db = Database()
    db.create_database(params)
    db.create_tables(params)
    db.insert_data_to_tables(params)

    dbm = DBManager()
    dbm.get_companies_and_vacancies_count(params)
    dbm.get_all_vacancies(params)
    dbm.get_avg_salary(params)
    dbm.get_vacancies_with_higher_salary(params)
    dbm.get_vacancies_with_keyword(params)


