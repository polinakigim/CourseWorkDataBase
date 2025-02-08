import requests
from src.abstract_classes import Parser

class HeadHunterAPI(Parser):

    def __init__(self):
        self.__url = 'https://api.hh.ru/'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = None
        self.employers = [3529, 80, 4518646, 3417276, 6063931, 1122462, 1740, 15478, 4329337,2180]

    def load_vacancies(self):
        """Метод загрузки данных вакансий из API сервиса"""
        emp_params = {
            "sort_by": "by_vacancies_open"
        }
        employers = []
        for employer_id in self.employers:
            emp_url = f"{self.__url}employers/{employer_id}"
            employer_info = requests.get(emp_url, headers=self.__headers, params=emp_params).json()
            employers.append(employer_info)

        return employers

    def correct_vacancy(self, num_vac):
        """Метод преобразования вакансий в корректный формат"""
        vac_url = f"{self.__url}vacancies"
        vacancies = []
        for emp in self.employers:
            vacancy_params = {
                "employer_id": emp,
                "per_page": num_vac,
                "only_with_salary": True
            }
            response = requests.get(vac_url, headers=self.__headers, params=vacancy_params)
            if response.status_code == 200:
                vac = response.json()["items"]
                vacancies.extend(vac)
            else:
                raise Exception(f"Ошибка {response.status_code}: {response.text}")
        return vacancies
