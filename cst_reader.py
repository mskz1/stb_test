import os
import sys
import glob

BUKKEN_CSV_NAME = "Structure\Analysis\Cooperation_Bukken.csv"
BUZAI_CSV_NAME = 'Structure\Analysis\Cooperation_Buzai.csv'
BUZAI_KIGOU_FOLDER_PATH = "Master"


class CasstData:
    def __init__(self):
        self.sec_data = {}
        self.buzai = {}

    def _load_section_data(self, f, res):
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
            res[section_name] = data

    def _load_buzai_data(self, folder_name):
        file_names = glob.glob(os.path.join(folder_name, BUZAI_KIGOU_FOLDER_PATH, 'list_buzaikigou_*.csv'))
        for file_name in file_names:
            with open(file_name) as f:
                kigou = os.path.basename(file_name)[:-4].split(sep='_')[-1]
                lines = f.readlines()[1:]  # １行目は捨てる
                self.buzai[kigou] = lines

    def _buzaikigou_file_names(self, folder_name):
        # 不要？
        # file_names = glob.glob(os.path.join(folder_name, BUZAI_KIGOU_FOLDER_PATH, 'list_buzaikigou_*.csv'))
        # return file_names
        pass

    def load(self, folder_name):
        with open(os.path.join(folder_name, BUKKEN_CSV_NAME)) as f:
            self._load_section_data(f, self.sec_data)
        with open(os.path.join(folder_name, BUZAI_CSV_NAME)) as f:
            self._load_section_data(f, self.sec_data)
        self._load_buzai_data(folder_name)

    def get_section_data(self, section, idx=None):
        if idx:
            data = self.sec_data[section]
            if len(data) == 1:
                return data[0].split(sep=',')[idx - 1]
            else:
                res = []
                for d in data:
                    res.append(d.split(sep=',')[idx - 1])
                return res
        else:
            return self.sec_data[section]

    def get_buzai_data(self, kigou, idx=None):
        if idx:
            data = self.buzai[kigou]
            if len(data) == 1:
                return data[0].split(sep=',')[idx - 1]
            else:
                res = []
                for d in data:
                    res.append(d.split(sep=',')[idx - 1])
                return res
        else:
            return self.buzai[kigou]


if __name__ == '__main__':
    # folder_name = "sample_cst"
    # with open(os.path.join(folder_name, BUKKEN_CSV_NAME)) as bukken:
    #     print(bukken.name)
    #
    # buzai = open(os.path.join(folder_name, BUZAI_CSV_NAME))
    # print(buzai.name)
    # buzai.close()
    pass
