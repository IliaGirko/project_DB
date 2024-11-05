import os

from dotenv import load_dotenv

from dev_db import CreationDB, CreationTable, RecordingDataToTable
from get_data_from_db import DBManager
from get_employer_hh import HeadHunterAPI
from get_vacancies_hh import HeadHunterVacancyAPI

load_dotenv()
host: str = os.getenv("HOST")
user: str = os.getenv("USER")
password: str = os.getenv("PASSWORD")
port: str = os.getenv("PORT")


def main() -> None:
    """Функция взаимодействия с пользователем"""
    user_input = input("Нажмите любую клавишу чтобы запустить меню: ")
    vacancy = HeadHunterVacancyAPI()
    employer = HeadHunterAPI()

    # print(employer.json_list())#получение списка работодателей
    result_list_employers = employer.json_list()
    list_vacancy = []
    for i in result_list_employers:
        list_vacancy.append(vacancy.json_list(i["id"]))

    # print(list_vacancy)#получение списка вакансий

    creation_database = CreationDB(host, user, password, port)
    creation_database.create_db()  # создание БД head_hunter

    creation_table = CreationTable(host, user, password, port)

    creation_table.create_table_employers()  # создание таблицы employers
    creation_table.create_table_vacancy()  # создание таблицы vacancy

    filling_out_the_table = RecordingDataToTable(host, user, password, port)
    filling_out_the_table.recording_to_table_employers(result_list_employers)  # заполнение таблицы employers
    filling_out_the_table.recording_to_table_vacancy(list_vacancy)  # заполнение таблицы vacancy

    a = DBManager(host, user, password, port)
    try:
        while user_input != "0":
            user_input = input(
                "Введите одну из соответствующих цифр чтобы запустить программу:\n"
                "1 - Выведет список всех компаний и количество вакансий у каждой компании.\n"
                "2 - Выведет список всех вакансий с указанием названия компании, "
                "названия вакансии и зарплаты и ссылки на вакансию.\n"
                "3 - Выведет среднюю зарплату по вакансиям.\n"
                "4 - Выведет список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                "5 - Выведет список всех вакансий, в названии которых содержатся переданные в метод слова, "
                "например python.\n"
                "0 - Завершение работы программы\n"
                "Укажите цифру: "
            )
            if user_input == "1":
                a.get_companies_and_vacancies_count()
                user_input = input(
                    "Введите '0' чтобы выйти из программы или '1' если хотите вернуться в меню\n" "Укажите цифру: "
                )
            elif user_input == "2":
                a.get_all_vacancies()
                user_input = input(
                    "Введите '0' чтобы выйти из программы или '1' если хотите вернуться в меню\n" "Укажите цифру: "
                )
            elif user_input == "3":
                a.get_avg_salary()
                user_input = input(
                    "Введите '0' чтобы выйти из программы или '1' если хотите вернуться в меню\n" "Укажите цифру: "
                )
            elif user_input == "4":
                a.get_vacancies_with_higher_salary()
                user_input = input(
                    "Введите '0' чтобы выйти из программы или '1' если хотите вернуться в меню\n" "Укажите цифру: "
                )
            elif user_input == "5":
                result = input("Введите слово для фильтрации: ")
                a.get_vacancies_with_keyword(result)
                user_input = input(
                    "Введите '0' чтобы выйти из программы или '1' если хотите вернуться в меню\n" "Укажите цифру: "
                )
        a.close_conn()
    except Exception as error:
        print(f"Возникло исключение: {error}")


if __name__ == "__main__":
    main()
