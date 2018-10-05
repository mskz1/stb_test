import pytest
import os
from pytest import approx
# from cst_reader import read_cst
from cst_reader import CasstData


def print_data(da, section):
    for l in da[section]:
        print(l.strip())


def test_load_data():
    cst = CasstData()
    cst.load('sample_cst')

    assert float(cst.get_section_data('KAIDAKA', idx=2)) == approx(100.)  # GLからの1FL高さ
    assert float(cst.get_section_data('KAIDAKA', idx=3)) == approx(5700.)  # GLからの2FL高さ
    assert float(cst.get_section_data('KAIDAKA', idx=6)) == approx(6500.)  # GLからの最高高さ
    assert float(cst.get_section_data('KEISAN', idx=21)) == approx(300.)  # BPLから1FL
    assert float(cst.get_section_data('KEISAN', idx=22)) == approx(310.)  # 1FLから基礎梁天
    assert float(cst.get_section_data('KEISAN', idx=23)) == approx(0.)  # 2FLから梁天
    assert float(cst.get_section_data('KEISAN', idx=24)) == approx(0.)  # 3FLから梁天

    assert cst.get_section_data('TORISHIN', idx=3) == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                       '11', '12', '13', '14', '15', '16', '17', '18', '19',
                                                       '20', '21', '22', '23', '24', '25', '26',
                                                       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                                       'M', 'N', 'O', "O'"]  # 通り心名

    assert cst.get_section_data('HASHIRA', idx=4)[:5] == ['C2AK', 'C3K', 'C2A', 'C2BK', 'C2K']
    assert cst.get_section_data('OOBARI', idx=4) == ['B44', 'B44', 'B44', 'B29', 'B15']
    assert cst.get_section_data('KOBARI', idx=4)[:5] == ['B34', 'B25', 'B25', 'B29', 'B34']
    assert cst.get_section_data('NOKIKETA_SAKUZU', idx=4)[:5] == ['P1', 'P1', 'P1', 'P1K', 'P1K']

    assert cst.get_buzai_data('HASHIRA', idx=1) == ['C1', 'C1K', 'C1A', 'C2', 'C2K', 'C2AK', 'C2BK', 'C3', 'C3K', 'C2A']
    assert cst.get_buzai_data('HASHIRA', idx=6)[0] == "□P-125x125x4.5"

    assert cst.get_buzai_data('OOBARI', idx=1) == ['B44', 'B29', 'B15']
    assert cst.get_buzai_data('OOBARI', idx=6) == ['H-446x199x8x12', 'H-298x149x5.5x8', 'H-150x75x5x7']
    assert cst.get_buzai_data('KOBARI', idx=1) == ['B24', 'B25', 'B29', 'B34', 'B39', 'B15']
    assert cst.get_buzai_data('ETC-NOKIGETA', idx=6) == ["C-125x50x20x2.3", "C-125x50x20x3.2"]


def test_file_names():
    # cst = CasstData()
    # files = cst._buzaikigou_file_names("sample_cst")
    # # for x in files:
    # #     print(os.path.basename(x))
    # for x in files:
    #     print(os.path.basename(x)[:-4].split(sep='_')[-1]) # 拡張子.csvを除き、_で区切られる最後の単語
    pass
