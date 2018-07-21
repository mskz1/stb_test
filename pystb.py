import xml.etree.ElementTree as ET

STB_NODE, STB_X_AXIS, STB_Y_AXIS, STB_STORY = 'StbNode', 'StbX_Axis', 'StbY_Axis', 'StbStory'
STB_COLUMN, STB_GIRDER, STB_BEAM, STB_BRACE = 'StbColumn', 'StbGirder', 'StbBeam', 'StbBrace'
STB_SEC_COLUMN_S, STB_SEC_STEEL_COLUMN = 'StbSecColumn_S', 'StbSecSteelColumn'
STB_SEC_BEAM_RC, STB_SEC_FIG = 'StbSecBeam_RC', 'StbSecFigure'
STB_SEC_BEAM_S, STB_SEC_STEEL_BEAM = 'StbSecBeam_S', 'StbSecSteelBeam'


class Stb:
    def __init__(self):
        self.stb = None

    def load_stb(self, file):
        with open(file, 'r', encoding='Shift_JIS') as f:
            self.stb = ET.fromstring(f.read())

    def save_stb(self, file):
        # tree = ET.ElementTree(self.stb)
        txt = ET.tostring(self.stb, encoding='unicode')
        with open(file, 'w', encoding='Shift_JIS') as f:
            # with open(file, 'w', encoding='UTF-8') as f:
            # tree.write(f, encoding='Shift_JIS')
            # LF = chr(10)
            f.write('<?xml version="1.0" encoding="Shift_JIS"?>' + chr(10))
            f.write(txt)

    def get_max_id(self, tag):
        ids = []
        if self.stb:
            for d in self.stb.iter(tag):
                ids.append(int(d.attrib['id']))
        return max(ids)

    def get_node_numbers(self):
        ids = []
        if self.stb:
            for n in self.stb.iter('StbNode'):
                ids.append(int(n.attrib['id']))
        return len(ids)

    def get_node_x(self, id):
        if self.stb:
            for n in self.stb.iter('StbNode'):
                if int(n.attrib['id']) == id:
                    return float(n.attrib['x'])
        return None

    def get_node_y(self, id):
        if self.stb:
            for n in self.stb.iter('StbNode'):
                if int(n.attrib['id']) == id:
                    return float(n.attrib['y'])
        return None

    def get_node_z(self, id):
        if self.stb:
            for n in self.stb.iter('StbNode'):
                if int(n.attrib['id']) == id:
                    return float(n.attrib['z'])
        return None

    def get_name_list(self, tag):
        res = []
        if self.stb:
            for d in self.stb.iter(tag):
                res.append(d.attrib['name'])
        return res

    def get_x_axis_distance(self, name=''):
        if self.stb:
            for d in self.stb.iter('StbX_Axis'):
                if d.attrib['name'] == name:
                    return float(d.attrib['distance'])

    def get_y_axis_distance(self, name=''):
        if self.stb:
            for d in self.stb.iter('StbY_Axis'):
                if d.attrib['name'] == name:
                    return float(d.attrib['distance'])

    def get_story_height(self, name=''):
        if self.stb:
            for d in self.stb.iter('StbStory'):
                if d.attrib['name'] == name:
                    return float(d.attrib['height'])

    def get_column_numbers(self):
        ids = []
        if self.stb:
            for n in self.stb.iter('StbColumn'):
                ids.append(int(n.attrib['id']))
        return len(ids)

    def get_element_attribute(self, tag, **kwargs):
        # **kwargsで複数のパラメーター条件を指定し、該当するエレメントの（アトリビュート）のリストを返す
        # 複数の条件の全てに該当するものが集められる。
        res = []
        for d in self.stb.iter(tag):
            flg = []
            for k, v in kwargs.items():
                if d.attrib[k] == v:
                    flg.append(True)
                else:
                    flg.append(False)
            if False not in flg:
                # res.append(d) #あるいはエレメントを返す？
                res.append(d.attrib)
        return res

    def get_elements(self, tag, **kwargs):
        # **kwargsで複数のパラメーター条件を指定し、該当するエレメントの（アトリビュート）のリストを返す
        # 複数の条件の全てに該当するものが集められる。
        res = []
        for d in self.stb.iter(tag):
            flg = []
            for k, v in kwargs.items():
                if d.attrib[k] == v:
                    flg.append(True)
                else:
                    flg.append(False)
            if False not in flg:
                res.append(d) #エレメントを返す？
                # res.append(d.attrib)
        return res



    def print_elements(self, tag):
        print('*** ', tag, ' ***')
        res = []
        for d in self.stb.iter(tag):
            res.append(d)
        for i in res:
            print(i.attrib)
