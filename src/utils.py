from typing import Any, Dict, List

import psycopg2
import requests

from src.config import config
from src.hh_api import HeadHunterAPI


def create_database() -> None:
    """Создание базы данных и таблиц для хранения данных об организациях и вакансиях"""
    params = config()
    params.pop("database", None)  # Удаляем database из параметров

    # Подключаемся к системной базе postgres
    conn = psycopg2.connect(database="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    # Получаем список существующих баз данных
    cur.execute("SELECT datname FROM pg_database")
    existing_databases = {row[0] for row in cur.fetchall()}

    if "test" not in existing_databases:
        cur.execute("CREATE DATABASE test")

    cur.close()
    conn.close()

    # Подключаемся к test
    params["database"] = "test"
    conn = psycopg2.connect(**params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from INT DEFAULT(0),
                salary_to INT DEFAULT(0),
                url VARCHAR(255),
                company_id INTEGER REFERENCES companies(company_id)
            )
        """
        )

    conn.commit()
    conn.close()


def save_data_to_database() -> None:
    """Сохранение данных об организациях и вакансиях в БД"""
    params = config()
    # params["database"] = database_name  # Устанавливаем правильное имя БД
    conn = psycopg2.connect(**params)

    hh = HeadHunterAPI()
    hh_company = hh.load_vacancies()
    hh_vacancy = hh.correct_vacancy(10)

    for employer in hh_company:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO companies (company_id, company_name)
                VALUES (%s, %s)
                ON CONFLICT (company_id) DO NOTHING
                RETURNING company_id
                """,
                (employer["id"], employer["name"]),
            )

            result = cur.fetchone()
            if result:
                company_id = result[0]
            else:
                continue

            for vacancy in hh_vacancy:
                if int(vacancy["employer"]["id"]) == int(company_id):
                    cur.execute(
                        """
                        INSERT INTO vacancies (company_id, vacancy_name, salary_from, salary_to, url)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            company_id,
                            vacancy["name"],
                            vacancy["salary"]["from"],
                            vacancy["salary"]["to"],
                            vacancy["url"],
                        ),
                    )

    conn.commit()
    conn.close()
