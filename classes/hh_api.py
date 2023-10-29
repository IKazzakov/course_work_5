import requests
import json
from config import PATH_TO_COMPANIES_JSON


class HeadHunterAPI():
    """Класс для работы с API Head Hunter"""
    API_vacancies_url = 'https://api.hh.ru/vacancies/'

    def __init__(self):
        """
        Инициализатор экземпляров класса для работы с API
        query_parameters: словарь с параметрами запроса
        """
        self.query_parameters = {
            'page': 0,
            'per_page': 100,
            'text': 'разработчик',
            'area': 113,
            'employer_id': self.get_employers_id_from_json(PATH_TO_COMPANIES_JSON),
            'only_with_salary': True
        }

    def get_vacancies_by_api(self):
        """Получает вакансии через API и сохраняет их в json"""
        response = requests.get(self.API_vacancies_url, params=self.query_parameters)
        if response.status_code == 200:
            response_json = response.json()
            vacancies = response_json['items']
            # Получаем список вакансий с выборкой по определенным параметрам
            list_vacancies = self.select_vacancy_parameters(vacancies)
            print(f'Получено {len(list_vacancies)} вакансий с платформы Head Hunter')
            # Сохраняем список вакансии в json
            self.save_vacancies_to_json(list_vacancies)
            return
        print(f'Ошибка {response.status_code} выполнения запроса')
        return []

    @staticmethod
    def get_employers_id_from_json(file_path):
        """Получает список id компаний из json"""
        with open(file_path) as json_file:
            data = json.load(json_file)
            companies_id = [company.get('company_HH_id') for company in data]
        return companies_id

    @staticmethod
    def select_vacancy_parameters(vacancies_data):
        """
           Выборка определенных параметров вакансии
           :param vacancies_data: список вакансий полученных через API
           :return: список вакансий по указанным параметрам
           """
        vacancies_by_parameters = []
        for vacancy in vacancies_data:
            vacancy_name = vacancy.get('name')
            company_id = vacancy.get('employer')['id']
            vacancy_city = vacancy.get('area')['name']
            vacancy_salary = vacancy.get('salary')
            if not vacancy_salary:
                salary_from = salary_to = 0
                currency = ''
            else:
                salary_from = vacancy_salary['from']
                salary_to = vacancy_salary['to']
                if not salary_from:
                    salary_from = salary_to
                if not salary_to:
                    salary_to = salary_from
                currency = vacancy_salary['currency']
            vacancy_url = vacancy.get('alternate_url')

            vacancy_card = {
                'vacancy_name': vacancy_name,
                'company_id': company_id,
                'vacancy_city': vacancy_city,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'vacancy_url': vacancy_url
            }
            vacancies_by_parameters.append(vacancy_card)
        return vacancies_by_parameters

    @staticmethod
    def save_vacancies_to_json(list_vacancies):
        """
        Сохраняет вакансии в json файл
        :param list_vacancies: список вакансий
        """
        try:
            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(list_vacancies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Ошибка записи в файл {e}')
