# TODO: требуется перекинуть в cj/deployment

import requests
from xml.etree import ElementTree as ET
from datetime import datetime
import sys
from lxml import etree
import os
import time
from prometheus_client import start_http_server, Gauge, Enum
import icu

# Настройка локали для считывания русской даты
import locale
locale.setlocale(locale.LC_ALL, '')

# Словари для хранения данных
data = {} # Time - Status
stat = {} # Status - [Time]

# Настройка для считывания времени
f = "%d %B, %A %H:%M"

# Замена месяцев
month = {
    "января": "январь"
}

bad_statuses = [
    "Запись на текущий день невозможна",
    "Время истекло. Запись недоступна", 
    "Время занято", 
    "Время, запись на которое осуществляется в поликлинике.", 
    "Запись возможна только на 14 дней вперед",
    "Запись: Ермейкин Сергей Владимирович Нажмите для отмены записи",
    "Запись будет возможна сегодня после 06:00"
    ]

def parse_date(s_date, fmt):
    # f = icu.
    f = icu.SimpleDateFormat(fmt, icu.Locale('ru'))
    return datetime.fromtimestamp(int(f.parse(s_date)))

def mznn_request(doctor_id):
    # Выполнение запроса
    response = requests.get(f'https://mis.mznn.ru/service/schedule/{doctor_id}/timetable')

    # Проверка статуса запроса
    if response.status_code != 200:
        print (f"Code: {response.status_code}")
        print (f"Text: {response.text}")
        sys.exit(1)

    # Нахождение таблицы со временем
    s = response.text
    # print (s)
    result = s[s.find('<table class="timeTable">')+1:s.find('</table>')]
    s = '<' + result + '</table>'
    s = s.replace("\n", "").replace("\t", "").replace("<br/>", " ")

    # Парсинг таблицы
    parser = etree.XMLParser(encoding='utf-8') # , recover=True
    table = etree.fromstring(s, parser=parser)

    rows = iter(table)
    # headers = [col.text for col in next(rows)]
    # Формирование данных для анализа
    for row in rows:
        for col in row:
            # print (col.attrib)
            dt = col.get("rel")
            status = col.get("title") 
            if dt is not None:
                for k, v in month.items():
                    dt = dt.replace(k, v)
                # print (datetime.today().strftime("%d %B, %A %H:%M"))
                # dt = parse_date(dt, f)
                # Рабочие строки
                dt = datetime.strptime(dt, f)
                dt = dt.replace(year=datetime.today().year)
                # print (dt)
                data[dt] = status

    # Формирование статистики
    for time, status in data.items():
        # print (f"{time} - {status}")
        if status in stat:
            stat[status].append (time)
        else:
            stat[status] = [time]

    return (data, stat)
    # # Вывод статистики по статусам
    # for status, times in stat.items():
    #     print (status, " - ", len(times))
    #     if status not in bad_statuses:
    #         print ("ALARM! ТРЕВОГА!")
    #         for time in times:
    #             print (f"ALARM TIME: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    #     if status == "Запись: Ермейкин Сергей Владимирович Нажмите для отмены записи":
    #         print (f"Занятое время: {times[0].strftime('%Y-%m-%d %H:%M:%S')}.")
    #     else:
    #         pass
    #         # print ("Ничего хорошего, начальник...")



"""Application exporter"""
class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, app_port=80, polling_interval_seconds=5):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.mznn_time_status = Gauge("mznn_time_status", "Статусы времени у врача", ["status"])

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Fetch raw status data from the application
        doctor_id = int(os.getenv("DOCTOR_ID", "520101000064490"))
        data, status = mznn_request(doctor_id)
        # print (data)
        # print ("---")
        # print (status)
        # print ("---")

        # Update Prometheus metrics with application metrics
        for status, times in stat.items():
            self.mznn_time_status.labels(status = status).set(len(times))

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "300"))
    app_port = int(os.getenv("APP_PORT", "80"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

    app_metrics = AppMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
