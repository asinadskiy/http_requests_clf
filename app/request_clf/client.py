"""
Клиент для отправки запросов

@author: asinadskiy
"""

import requests, json, csv

def predict_one(url=None, data=None):
    """
    Отправка запроса на сервер для получения предсказания класса элемента

    Parameters
    ----------
    url : str
        Адрес сервиса предсказаний.
    data : str
        Набор признаков элемента - строка в JSON-формате.

    Returns
    -------
    label : str
        Предсказанная метка класса.

    """
    headers = {'Content-Type': 'application/json'}
    label = requests.post(url, headers=headers, data=data).text
    return label
    

def send_all_csv(url, csv_file_path):
    """
    Отправка CSV-файла и получение ответов.

    Parameters
    ----------
    url : str
        Адрес сервиса предсказаний.
    filename : str
        Путь к CSV-файлу с данными.

    Returns
    -------
    labels : list
        Метки класса для каждой строки из входного файла.

    """

    labels = []
    with open(csv_file_path, encoding='utf-8') as csv_file: 
        csvReader = csv.DictReader(csv_file) 
        for row in csvReader:
            labels.append(predict_one(url, json.dumps(row)))
    return labels
