import os
import sys

BUKKEN_CSV_NAME = "Structure\Analysis\Cooperation_Bukken.csv"
BUZAI_CSV_NAME = 'Structure\Analysis\Cooperation_Buzai.csv'


def read_cst(folder_name):
    res = {}
    with open(os.path.join(folder_name, BUKKEN_CSV_NAME)) as f:
        load_section_data(f, res)
    with open(os.path.join(folder_name, BUZAI_CSV_NAME)) as f:
        load_section_data(f,res)
    return res




def load_section_data(f, res):
    lines = f.readlines()
    section_index = []
    for i, line in enumerate(lines):
        if line[:7] == "SECTION":
            section_index.append(i)
    for i, idx in enumerate(section_index):
        section_name = lines[idx].split(sep=',')[1]
        if i < len(section_index) - 1:
            data = lines[idx + 1:section_index[i + 1]]
        else:
            data = lines[idx + 1:]
        # print(section_name)
        # print(data)
        res[section_name] = data


if __name__ == '__main__':
    # folder_name = "sample_cst"
    # with open(os.path.join(folder_name, BUKKEN_CSV_NAME)) as bukken:
    #     print(bukken.name)
    #
    # buzai = open(os.path.join(folder_name, BUZAI_CSV_NAME))
    # print(buzai.name)
    # buzai.close()
    pass
