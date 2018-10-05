import pytest
from pytest import approx

from cst_reader import read_cst


def print_data(da,section):
    for l in da[section]:
        print(l.strip())


def test_csv_1():
    #     s = """SECTION,KAIDAKA,1
    # 1,100.000000,5700.000000,0.000000,5700.000000,6500.000000,1200.000000
    # """
    #     lines = s.split(sep='\n')
    #     print(lines)
    #     sec_name = lines[0].split(sep=',')[1]
    #     print(sec_name)

    pass


def test_reading():
    cst = read_cst("sample_cst")
    # print(cst['KAIDAKA'])
    # print_data(cst,'KAIDAKA')
    # print_data(cst,'TORISHIN')
    print_data(cst,'GAIHEKI-HONTAI')
