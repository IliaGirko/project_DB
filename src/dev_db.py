import os
from abc import ABC, abstractmethod

import psycopg2
from dotenv import load_dotenv

load_dotenv()
host: str = os.getenv("HOST")
user: str = os.getenv("USER")
password: str = os.getenv("PASSWORD")
port: str = os.getenv("PORT")


class CreateDB(ABC):
    """Абстрактный класс взаимодействия с БД"""

    @abstractmethod
    # """Абстрактный метод создания новой базы данных"""
    def create_db(self) -> None:
        pass


class CreationDB(CreateDB):
    """Класс создания БД"""

    def __init__(self, host, user, password, port):
        """Магический метод инициализации параметров для подключения к БД"""
        self._host = host
        self._user = user
        self.__password = password
        self._port = port

    def create_db(self) -> None:
        """Метод создания новой БД 'head_hunter'"""
        conn = psycopg2.connect(
            dbname="postgres", host=self._host, user=self._user, password=self.__password, port=self._port
        )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("DROP DATABASE head_hunter;")
            cur.execute("CREATE DATABASE head_hunter;")
        except Exception:
            cur.execute("CREATE DATABASE head_hunter;")

        cur.close()
        conn.close()


class CreateTable(ABC):
    """Абстрактный класс создания таблиц"""

    @abstractmethod
    # """Абстрактный метод создания таблицы с работодателями"""
    def create_table_employers(self) -> None:
        pass

    @abstractmethod
    # """Абстрактный метод создания таблицы с вакансиями"""
    def create_table_vacancy(self) -> None:
        pass


class CreationTable(CreateTable):
    """Класс создания таблиц в  БД head hunter"""

    def __init__(self, host, user, password, port):
        """Магический метод инициализации параметров для подключения к БД"""
        self._host = host
        self._user = user
        self.__password = password
        self._port = port

    def create_table_employers(self) -> None:
        """Метод создания таблицы работодатели"""
        conn = psycopg2.connect(dbname="head_hunter", host=host, user=user, password=password, port=port)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE employers(
            employer_id INTEGER PRIMARY KEY,
            employer_name VARCHAR NOT NULL,
            url_to_employer TEXT NOT NULL,
            open_vacancies INTEGER
            )"""
            )
        conn.close()

    def create_table_vacancy(self) -> None:
        """Метод создания таблицы вакансии"""
        conn = psycopg2.connect(dbname="head_hunter", host=host, user=user, password=password, port=port)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE vacancy(
            employer_id INTEGER ,
            vacancy_name TEXT,
            salary_from INTEGER,
            salary_to INTEGER,
            url_to_vacancy TEXT,
            FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
            )"""
            )
        conn.close()


class RecordData(ABC):
    """Абстрактный класс записи данных в таблицы"""

    @abstractmethod
    # """Абстрактный метод записи данных в таблицу работодатели"""
    def recording_to_table_employers(self) -> None:
        pass

    @abstractmethod
    # """Абстрактный метод записи данных в таблицу вакансии"""
    def recording_to_table_vacancy(self) -> None:
        pass


class RecordingDataToTable(RecordData):
    """Класс наполнения таблиц данными"""

    def __init__(self, host, user, password, port):
        """Магический метод инициализации параметров для подключения к БД"""
        self._host = host
        self._user = user
        self.__password = password
        self._port = port

    def recording_to_table_employers(self, employers_data) -> None:
        """Метод наполнения таблицы работодатели данными с сайта hh.ru"""
        conn = psycopg2.connect(dbname="head_hunter", host=host, user=user, password=password, port=port)
        conn.autocommit = True
        with conn.cursor() as cur:
            for i in employers_data:
                employer_id = i.get("id")
                employer_name = i.get("name")
                url_to_employer = i.get("alternate_url")
                open_vacancies = i.get("open_vacancies")
                cur.execute(
                    """INSERT INTO employers(employer_id, employer_name,
                 url_to_employer, open_vacancies) VALUES(%s, %s, %s, %s)""",
                    (employer_id, employer_name, url_to_employer, open_vacancies),
                )

        conn.close()

    def recording_to_table_vacancy(self, vacancy_data) -> None:
        """Метод наполнения таблицы вакансии данными с сайта hh.ru"""
        conn = psycopg2.connect(dbname="head_hunter", host=host, user=user, password=password, port=port)
        conn.autocommit = True
        with conn.cursor() as cur:
            for n in range(len(vacancy_data)):
                for i in vacancy_data[n]:
                    employer_id = i.get("employer").get("id")
                    vacancy_name = i.get("name")
                    if not i.get("salary"):
                        salary_from = None
                        salary_to = None
                    else:
                        salary_from = i.get("salary").get("from")
                        salary_to = i.get("salary").get("to")
                    url_to_vacancy = i.get("alternate_url")
                    cur.execute(
                        """INSERT INTO vacancy(employer_id, vacancy_name,
                         salary_from, salary_to, url_to_vacancy) VALUES(%s, %s, %s, %s, %s)""",
                        (employer_id, vacancy_name, salary_from, salary_to, url_to_vacancy),
                    )
        conn.close()


if __name__ == "__main__":
    a = CreationDB(host, user, password, port)
    print(a.create_db())
