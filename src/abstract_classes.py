from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для получения публичного API hh.ru"""

    @abstractmethod
    def load_vacancies(self) -> None:
        """Метод загрузки вакансий"""
        pass

    @abstractmethod
    def correct_vacancy(self, keyword: str) -> None:
        pass


class DBManagerABC(ABC):
    """Абстрактный класс для работы с База данных"""

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """Метод для получения всех компаний и количество вакансий у каждой компании"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """Метод получения всех вакансий с указанием: название компании, название вакансии, зарплата, ссылка на вакансию"""
        pass

    @abstractmethod
    def get_avg_salary(self):
        """Метод получения средней зарплаты по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """Метод получения выше средней зарплаты по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword):
        """Метод получения списка всех вакансий в названии которых есть ключевые слова"""
        pass
