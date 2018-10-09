import os
import sys
import glob
from pystb import Stb

BUKKEN_CSV_NAME = "Structure\Analysis\Cooperation_Bukken.csv"
BUZAI_CSV_NAME = 'Structure\Analysis\Cooperation_Buzai.csv'
BUZAI_KIGOU_FOLDER_PATH = "Master"


class CasstData:
    def __init__(self):
        self.stb = Stb()
        self.nodes = {}
        self.height = {}  # 階の高さ {'1FL':100, '2FL':3500...}
        self.sec_data = {}
        self.buzai = {}

    def get_free_node_id(self):
        # node id は連続であると仮定
        return (len(self.nodes) + 1)

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

    def get_grids(self):
        # 通り名、距離をリストで返す
        # ['A', 'B', 'C',...], [0.0, 2000.0, ...],['1', '2', '3'...],[0.0, 1400.0, 3400.0,...]
        x_names = []
        y_names = []
        x_dist = []
        y_dist = []

        direcs = self.get_section_data('TORISHIN', idx=2)
        names = self.get_section_data('TORISHIN', idx=3)
        dists = self.get_section_data('TORISHIN', idx=4)
        is_grids = self.get_section_data('TORISHIN', idx=5)

        for is_grid in is_grids:
            direc, name, dist, = direcs.pop(0), names.pop(0), dists.pop(0)
            if is_grid.strip() == "1":
                if direc.strip() == "1":
                    x_names.append(name)
                    x_dist.append(float(dist))
                if direc.strip() == "0":
                    y_names.append(name)
                    y_dist.append(float(dist))
        return x_names, x_dist, y_names, y_dist

    def gen_xy_coords(self, xdata, ydata):
        # 不要か
        res = []
        for x in xdata:
            res.append((x, ydata[0]))
        for y in ydata:
            res.append((xdata[0], y))
        return res

    def gen_grid_nodes(self):
        # 不要か
        xnames, xdists, ynames, ydists = self.get_grids()
        xypoints = self.gen_xy_coords(xdists, ydists)
        nid = len(self.nodes) + 1
        for xy in xypoints:
            self.nodes[nid] = (xy[0], xy[1], 0)

    def gen_stb(self):
        self.stb.new_stb()

    def add_node(self, x, y, z):
        nid = self.get_free_node_id()
        self.nodes[nid] = (x, y, z)
        if self.stb:
            self.stb.add_node(nid, x, y, z)
        return nid

    def gen_stb_grids(self):
        self.stb.add_node_tmp1()  # gridにnode_listがないと変換されないため、ダミーとして作る
        xnames, xdists, ynames, ydists = self.get_grids()
        for i, name in enumerate(xnames):
            self.stb.add_grid('StbX_Axis', id=i + 101, name=name, distance=xdists[i])
        for i, name in enumerate(ynames):
            self.stb.add_grid('StbY_Axis', id=i+1, name=name, distance=ydists[i])

    def _set_story_height(self):
        names = ['1FL', '2FL', '3FL']
        heights = [float(self.get_section_data('KAIDAKA', idx=2)), float(self.get_section_data('KAIDAKA', idx=3)),
                   float(self.get_section_data('KAIDAKA', idx=4))]
        for i, name in enumerate(names):
            self.height[name] = heights[i]

    def gen_stb_stories(self):
        self._set_story_height()
        i = 1
        for k, v in self.height.items():
            if v != 0.:
                self.stb.add_story(id=i, name=k, height=v)
                i += 1

    def gen_stb_model(self):
        # STBモデルを生成
        self._set_story_height()

        # 柱
        data = self.get_section_data('HASHIRA')
        cid = 1
        for line in data:
            itm = line.split(',')
            kai, fugou, xc, yc, sagari = itm[1], itm[3], float(itm[4]), float(itm[5]), float(itm[6])
            zc_u = self.height[kai] - sagari
            l_kai = '2FL'
            if kai == '2FL':
                l_kai = '1FL'
            zc_l = self.height[l_kai]
            n1 = self.add_node(xc, yc, zc_l)
            n2 = self.add_node(xc, yc, zc_u)
            self.stb.add_column(cid, fugou, n1, n2, '1')
            cid += 1



if __name__ == '__main__':
    # folder_name = "sample_cst"
    # with open(os.path.join(folder_name, BUKKEN_CSV_NAME)) as bukken:
    #     print(bukken.name)
    #
    # buzai = open(os.path.join(folder_name, BUZAI_CSV_NAME))
    # print(buzai.name)
    # buzai.close()
    pass
