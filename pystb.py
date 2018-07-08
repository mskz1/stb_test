import xml.etree.ElementTree as ET

STB_NODE, STB_X_AXIS, STB_Y_AXIS, STB_STORY = 'StbNode', 'StbX_Axis', 'StbY_Axis', 'StbStory'
STB_COLUMN, STB_GIRDER, STB_BEAM, STB_BRACE = 'StbColumn', 'StbGirder', 'StbBeam', 'StbBrace'


class Stb:
    def __init__(self):
        self.stb = None

    def load_stb(self, file):
        with open(file, 'r', encoding='Shift_JIS') as f:
            self.stb = ET.fromstring(f.read())

    def get_max_node_id(self):
        ids = []
        if self.stb:
            for n in self.stb.iter('StbNode'):
                ids.append(int(n.attrib['id']))
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

    def get_x_axis_names(self):
        res = []
        if self.stb:
            for d in self.stb.iter('StbX_Axis'):
                res.append(d.attrib['name'])
        return res

    def get_y_axis_names(self):
        res = []
        if self.stb:
            for d in self.stb.iter('StbY_Axis'):
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

    def get_story_names(self):
        res = []
        if self.stb:
            for d in self.stb.iter('StbStory'):
                res.append(d.attrib['name'])
        return res

    def get_story_height(self, name=''):
        if self.stb:
            for d in self.stb.iter('StbStory'):
                if d.attrib['name'] == name:
                    return float(d.attrib['height'])

    def get_max_column_id(self):
        ids = []
        if self.stb:
            for n in self.stb.iter('StbColumn'):
                ids.append(int(n.attrib['id']))
        return max(ids)

    def get_column_numbers(self):
        ids = []
        if self.stb:
            for n in self.stb.iter('StbColumn'):
                ids.append(int(n.attrib['id']))
        return len(ids)

    def get_element_attribute(self, tag, **kwargs):
        for d in self.stb.iter(tag):
            for k, v in kwargs.items():
                if d.attrib[k] == v:
                    return d.attrib

    def get_elements(self,tag, **kwargs):
        # **kwargsで複数のパラメーター条件を指定し、該当するエレメントのリストを返す？
        # 複数の条件のいずれかに該当するものが集められる。
        res = []
        for k, v in kwargs.items():
            for d in self.stb.iter(tag):
                if d.attrib[k] == v:
                    # res.append(d)
                    res.append(d.attrib)
        return res

