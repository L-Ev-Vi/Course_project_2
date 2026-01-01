import os
import time

from src.api_hh import HH
from src.filling_in_job_information import FillingInJobInformation
from src.filling_in_request_data import FillingInRequestData
from src.get_top_vacancies import get_top_vacancies
from src.greeting_time_day import GreetingTimeDay
from src.json_saver import JSONSaver
from src.print_vacancies import print_vacancies
from src.sort_vacancies import sort_vacancies
from src.vacancy import Vacancy


def user_interface() -> None:
    """Функция для взаимодействия с пользователем"""
    print(GreetingTimeDay.get_a_greeting())
    while True:
        action = input(
            "Выберите возможные действия\n"
            "1 — Создать вакансию\n"
            "2 — Выполнить поиск по вакансиям\n"
            "3 — Просмотреть файлы с вакансиями\n"
            "4 — Выйти из программы\n"
            "->"
        )
        if action == "1":
            print(
                "Для создания вакансии необходимо указать следующие параметры: название вакансии*, "
                "ссылку на вакансию*, \n"
                "заработную плату (значение заработной платы можно оставить пустым), описание вакансии*\n "
                "[параметры обязательные для заполнения отмечены *].\n"
                "Пример заполнения данных при создании вакансии\n"
                "(Python Developer, <https://hh.ru/vacancy/123456>, 100 000-150 000 , "
                "Требования: опыт работы от 3 лет)\n"
            )
            job_data = FillingInJobInformation()
            vacancy1 = Vacancy(*job_data.getting_data())
            print(f"Создана вакансия {vacancy1.get_job_properties["name"]} c ID-{vacancy1.get_job_properties["id"]}")

            save_request = input("Сохранить созданную вакансию в файл '.json'?\n" "Y = 'yes'/ N = 'no'->")
            if save_request.lower() == "y":
                if len(os.listdir("data")) == 0:
                    file_to_save = input(
                        "Введите имя файл для сохранения созданной вакансии \n"
                        "или оставите значение пустым (будет использоваться файл по умолчанию 'job_information')\n"
                        "->"
                    )
                    if file_to_save:
                        json_saver = JSONSaver(file_to_save)
                    else:
                        json_saver = JSONSaver()
                    json_saver.add_vacancy(vacancy1)
                    print(
                        f"Выполнено сохранение вакансии {vacancy1.get_job_properties["name"]} "
                        f"c ID-{vacancy1.get_job_properties["id"]} \n"
                    )
                else:
                    print(
                        "Выберите имя файл из списка\n"
                        "или укажите имя нового файл, для сохранения созданной вакансии \n"
                        "если оставить значение пустым (будет использоваться файл по умолчанию 'job_information')"
                    )
                    for i, file in enumerate(os.listdir("data")):
                        print(f"{i + 1}) {file}")
                    file_to_save = input("->")
                    if file_to_save:
                        if file_to_save.isdigit():
                            if 0 < int(file_to_save) <= (len(os.listdir("data")) + 1):
                                file_to_save = os.listdir("data")[int(file_to_save) - 1][:-5]
                        json_saver = JSONSaver(file_to_save)
                    else:
                        json_saver = JSONSaver()
                    json_saver.add_vacancy(vacancy1)
                    print(
                        f"Выполнено сохранение вакансии {vacancy1.get_job_properties["name"]} "
                        f"c ID-{vacancy1.get_job_properties["id"]} \n"
                    )
                delete_vacancy = input(
                    f"Удалит вакансию {vacancy1.get_job_properties["name"]} "
                    f"c ID-{vacancy1.get_job_properties["id"]} из файла? \n"
                    f"Y = 'yes'/ N = 'no'->"
                )
                if delete_vacancy.lower() == "y":
                    json_saver.delete_vacancy(vacancy1)
                    print(
                        f"Выполнено удаление вакансии {vacancy1.get_job_properties["name"]} "
                        f"c ID-{vacancy1.get_job_properties["id"]} \n"
                    )
            time.sleep(2)
            print()
        elif action == "2":
            information_request = FillingInRequestData()
            search_query, top_n, keyword, salary_range_min, salary_range_max = information_request.getting_data()
            hh_api = HH()
            hh_vacancies = Vacancy.cast_to_object_list(hh_api.get_vacancies(search_query))
            if len(os.listdir("data")) == 0:
                file_to_save = input(
                    "Введите имя файл для сохранения вакансий \n"
                    "или оставите значение пустым (будет использоваться файл по умолчанию 'job_information')\n"
                    "->"
                )
                if file_to_save:
                    json_saver = JSONSaver(file_to_save)
                else:
                    json_saver = JSONSaver()
            else:
                print(
                    "Выберите имя файл из списка\n"
                    "или укажите имя нового файл, для сохранения созданной вакансий \n"
                    "если оставить значение пустым (будет использоваться файл по умолчанию 'job_information')"
                )
                for i, file in enumerate(os.listdir("data")):
                    print(f"{i + 1}) {file}")
                file_to_save = input("->")
                if file_to_save:
                    if file_to_save.isdigit():
                        if 0 < int(file_to_save) <= (len(os.listdir("data")) + 1):
                            file_to_save = os.listdir("data")[int(file_to_save) - 1][:-5]
                    json_saver = JSONSaver(file_to_save)
                else:
                    json_saver = JSONSaver()
            for vacancy in hh_vacancies:
                json_saver.add_vacancy(vacancy)
            sorted_vacancies = sort_vacancies(
                json_saver.get_job_information(keyword, salary_range_min, salary_range_max)
            )
            print_vacancies(get_top_vacancies(sorted_vacancies, top_n))
            get_entire_list = input("Просмотреть весь список вакансий?\n" "Y = 'yes'/ N = 'no'->")
            if get_entire_list.lower() == "y":
                print_vacancies(sorted_vacancies)
                time.sleep(3)
                print()
        elif action == "3":
            files_vacancies = os.listdir("data")
            if len(files_vacancies) == 0:
                print("Не найдено ни одного файла с вакансиями!")
            else:
                print("Выберите имя файла из списка")
                for i, file in enumerate(files_vacancies):
                    print(f"{i + 1}) {file}")
                while True:
                    file_ = input("->")
                    if file_.isdigit():
                        if 0 < int(file_) <= (len(files_vacancies) + 1):
                            file_name = files_vacancies[int(file_) - 1][:-5]
                            json_saver = JSONSaver(file_name)
                            print_vacancies(json_saver.get_job_information())
                            time.sleep(2)
                            if len(json_saver.get_job_information()) == 0:
                                print("Список вакансий пуст.")
                            else:
                                clear_list = input("Удалить все вакансии из файла?\n" "Y = 'yes'/ N = 'no'->")
                                if clear_list.lower() == "y":
                                    json_saver.delete_content()
                            delete_a_file = input(
                                f"Удалить файл {files_vacancies[int(file_) - 1]}?\n" "Y = 'yes'/ N = 'no'->"
                            )
                            if delete_a_file.lower() == "y":
                                os.remove(f"data/{files_vacancies[int(file_) - 1]}")
                                print(f"Выполнено удаление файла {files_vacancies[int(file_) - 1]}")
                                break
                            else:
                                break
                        else:
                            print("Ошибка ввод!")
                    else:
                        print("Ошибка ввод!")
            time.sleep(2)
            print()
        elif action == "4":
            break


if __name__ == "__main__":
    user_interface()
