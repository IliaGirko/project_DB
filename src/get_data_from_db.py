from abc import ABC, abstractmethod

import psycopg2


class UsingDB(ABC):
    """Абстрактный класс взаимодействия с БД с целью получения данных"""

    @abstractmethod
    # """Абстрактный метод получает список всех компаний и
    # количество вакансий у каждой компании."""
    def get_companies_and_vacancies_count(self) -> None:
        pass

    @abstractmethod
    # """Абстрактный метод получает список всех вакансий с указанием
    # названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
    def get_all_vacancies(self) -> None:
        pass

    @abstractmethod
    # """Абстрактный метод получает среднюю зарплату по вакансиям."""
    def get_avg_salary(self) -> None:
        pass

    @abstractmethod
    # """Абстрактный метод получает список всех вакансий,
    # у которых зарплата выше средней по всем вакансиям."""
    def get_vacancies_with_higher_salary(self) -> None:
        pass

    @abstractmethod
    # """Абстрактный метод получает список всех вакансий,
    # в названии которых содержатся переданные в метод слова, например python."""
    def get_vacancies_with_keyword(self) -> None:
        pass


class DBManager(UsingDB):
    """Класс взаимодействия с БД"""

    def __init__(self, host, user, password, port):
        self._host = host
        self._user = user
        self.__password = password
        self._port = port
        self.conn = psycopg2.connect(
            dbname="head_hunter", host=self._host, user=self._user, password=self.__password, port=self._port
        )

    def get_companies_and_vacancies_count(self) -> None:
        """Метод получает список всех компаний и
        количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT employer_name, open_vacancies FROM employers""")
            for name, quantity in cur:
                print(f"Название компании: {name}, количество вакансий: {quantity}")

    def get_all_vacancies(self) -> None:
        """Метод получает список всех вакансий с указанием
        названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT employer_name, vacancy_name, salary_from, salary_to, url_to_vacancy
            FROM vacancy
            JOIN employers USING(employer_id)"""
            )
            for e_name, v_name, sal_f, sal_to, url in cur:
                if not sal_f:
                    sal_f = 0
                if not sal_to:
                    sal_to = sal_f
                print(
                    f"Название компании: {e_name}, название вакансии: {v_name}, зарплата от {sal_f} до {sal_to},"
                    f" ссылка на вакансию {url}\n"
                )

    def get_avg_salary(self) -> None:
        """Метод получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT AVG(salary_from + salary_to)
                        FROM vacancy
                        WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL"""
            )
            for i in cur:
                print(f"Средняя зарплата по вакансиям: {round(i[0], 2)}")

    def get_vacancies_with_higher_salary(self) -> None:
        """Метод получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT vacancy_name, salary_from, salary_to, url_to_vacancy
            FROM vacancy
            WHERE salary_to > (SELECT AVG(salary_from + salary_to) FROM vacancy)"""
            )
            for v_name, sal_f, sal_to, url in cur:
                if not sal_f:
                    sal_f = 0
                if not sal_to:
                    continue
                print(f"Название вакансии: {v_name}, зарплата от {sal_f} до {sal_to}," f" ссылка на вакансию {url}\n")

    def get_vacancies_with_keyword(self, word) -> None:
        """Метод получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT vacancy_name, salary_from, salary_to, url_to_vacancy FROM vacancy WHERE vacancy_name ILIKE '%{word}%'"
            )
            for v_name, sal_f, sal_to, url in cur:
                if not sal_f:
                    sal_f = 0
                if not sal_to:
                    sal_to = sal_f
                print(f"Название вакансии: {v_name}, зарплата от {sal_f} до {sal_to}," f" ссылка на вакансию {url}\n")

    def close_conn(self) -> None:
        """Метод закрывает соединение с БД"""
        self.conn.close()
