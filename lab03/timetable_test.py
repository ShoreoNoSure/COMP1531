#This is the test file for timetable.py
from timetable import timetable
from datetime import date, time, datetime

def test_example():
    timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]

def test_injective():
    timetable([date(2020,3,15)], [time(12,00)]) == [datetime(2020,3,15,12,00)]

def test_empty():
    timetable([], []) == []

