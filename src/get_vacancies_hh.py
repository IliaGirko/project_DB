from abc import ABC, abstractmethod
from typing import Any

import requests

from get_employer_hh import HeadHunterAPI


class ImportVacancyAPI(ABC):
    """Абстрактный класс импорта с использованием API"""

    @abstractmethod
    # """Абстрактный метод получения ответа от API"""
    def _ImportAPI__get_vacancies(self, keyword: str) -> dict[list[dict[Any]]] | None:
        pass

    @abstractmethod
    # """Абстрактный метод преобразование ответа от API в json формат"""
    def json_list(self, keyword: str) -> list[dict[Any]] | list:
        pass


class HeadHunterVacancyAPI(ImportVacancyAPI):
    """Класс работы с вакансиями с сайта hh.ru"""

    def __init__(self):
        """Инициализация параметров для работы с api hh.ru"""
        self.__url: str = "https://api.hh.ru/vacancies"
        self.__params: dict[str, Any] = {"page": 0, "per_page": 5, "employer_id": ""}

    def _ImportAPI__get_vacancies(self, keyword: str) -> Any:
        """В методе получаются вакансии с сайта HH.ru'"""
        if isinstance(keyword, str):
            self.__params["employer_id"] = keyword
            response: Any = requests.get(self.__url, params=self.__params)
            if response.status_code == 200:
                return response
            else:
                raise Exception("Не удалось подключиться к API HH")
        else:
            raise AttributeError("Не корректный id работодателя")

    def json_list(self, keyword: str) -> list[dict[str, Any]] | list:
        """Метод преобразует ответ с сайта hh.ru в формат строки json"""
        try:
            return self._ImportAPI__get_vacancies(keyword).json().get("items")
        except Exception as e:
            print(e)
            return []


if __name__ == "__main__":
    a = HeadHunterVacancyAPI()
    employer = HeadHunterAPI()
    result = employer.json_list()
    list_vacancy = []
    for i in result:
        list_vacancy.append(a.json_list(i["id"]))
    print(list_vacancy[0])
