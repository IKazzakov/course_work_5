# course_work_5
Проект по БД

## Предварительные настройки

Файл зависимостей называется "requirements.txt". В этом файле перечисляются все библиотеки и их версии, необходимые для работы проекта. Для установки зависимостей из "requirements.txt", выполните:
pip install -r requirements.txt

Для корректной работы БД и подключения необходимо создать и заполнить своими данными файл "database.ini":  
[postgresql] #секция  
- host=localhost #ваш хост для подключения  
- user=postgres #ваше имя пользователя  
- password=password #ваш пароль  
- port=5432 #ваш порт  
т.к это конфиденциальная информация не забудьте добавить файл в .gitignore.

Файл company.json содержит информацию о десяти заранее выбранных компаниях (id компании на hh.ru, название компании).


## Класс HeadHunterAPI()  
Получает вакансии через API.ru, сохраняет вакансии в json файл  
## Класс Database()  
Создает новую базу данных  
Создает таблицы companies и vacancies  
Заполняет таблицы данными из json файлов  
## Класс DBManager()  
Имеет следующие методы:  
+ get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.  
+ get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.  
+ get_avg_salary() — получает среднюю зарплату по вакансиям.  
+ get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.  
+ get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.  
