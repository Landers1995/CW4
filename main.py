from pathlib import Path
from src.api_clients.base import VacancyApiClient
from src.api_clients import HeadHunterAPI
from src.file_connector import JSONConnector
from src.file_connector.base import FileConnector
from prettytable import PrettyTable


BASE_PATH = Path(__file__).parent
VACANCIES_PATH_FILE = BASE_PATH.joinpath('vacancies.json')
api_client: VacancyApiClient = HeadHunterAPI()
json_connector: FileConnector = JSONConnector(VACANCIES_PATH_FILE)


def loading_vacancies():
    search_word = input('Ключевое слово для поиска: ')
    vacancies = api_client.get_vacancies(search_word.lower())
    for vac in vacancies:
        json_connector.add_vacancy(vac)


def display_top_10_vacancies():
    vacancies = json_connector.get_vacancies()
    t = PrettyTable(['name', 'url', 'employer', 'salary'])

    for vac in sorted(vacancies, key=lambda x: x.salary, reverse=True)[:10]:
        salary = '{_from} -> {_to}, {currency}'.format(
            _from=vac.salary.salary_from or 0,
            _to=vac.salary.salary_to or 0,
            currency=vac.salary.currency,
        )
        t.add_row([vac.name, vac.url, vac.employer_name, salary])

    print(t)


WELCOME_MESSAGE = """
Доро пожаловать в программу, выберте действия:
1. Загрузить вакансии в файл по ключевому слову
2. Вывести топ 10 вакансий из файла
3. Выйти
"""

MAPPING = {'1': loading_vacancies, '2': display_top_10_vacancies}


def main():
    while True:
        print(WELCOME_MESSAGE)
        user_input = input()
        if not user_input.isdigit():
            continue

        if user_input in MAPPING:
            callback = MAPPING[user_input]
            callback()

        elif user_input == '0':
            break


if __name__ == '__main__':
    main()
