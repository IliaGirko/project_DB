from abc import ABC, abstractmethod
from typing import Any

import requests


class ImportEmployerHH(ABC):
    """Абстрактный класс получения информации о работодателях с сайта hh.ru"""

    @abstractmethod
    # """Абстрактный метод подключения к API hh"""
    def get_employer(self, key) -> Any:
        pass

    @abstractmethod
    # """Абстрактный метод преобразование ответа от API в json формат"""
    def json_list(self) -> list[dict[str, Any]] | list:
        pass


class HeadHunterAPI(ImportEmployerHH):
    """Класс работы с API head hunter"""

    def get_employer(self, key) -> Any | None:
        """Метод получения информации о работодателях"""
        response = requests.get(f"https://api.hh.ru/employers/{key}")
        if response.status_code == 200:
            return response

    def json_list(self) -> list[dict[str, Any]] | list:
        """Метод преобразования ответа, с сайта hh.ru, о работодателях в json формат"""
        list_employers: list[str] = [
            "906391",
            "9582396",
            "2324020",
            "4596113",
            "2355830",
            "5557093",
            "8893124",
            "3529809",
            "4046921",
            "9938436",
        ]
        result: list = []
        for i in list_employers:
            result.append(self.get_employer(i).json())
        return result


if __name__ == "__main__":
    a = HeadHunterAPI()
    print(a.json_list())
