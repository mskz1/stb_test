import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.lines as ml
import matplotlib.patches as mp

STB_NODE, STB_X_AXIS, STB_Y_AXIS, STB_STORY = 'StbNode', 'StbX_Axis', 'StbY_Axis', 'StbStory'
STB_COLUMN, STB_GIRDER, STB_BEAM, STB_BRACE = 'StbColumn', 'StbGirder', 'StbBeam', 'StbBrace'
STB_SEC_COLUMN_S, STB_SEC_STEEL_COLUMN = 'StbSecColumn_S', 'StbSecSteelColumn'
STB_SEC_BEAM_RC, STB_SEC_FIG = 'StbSecBeam_RC', 'StbSecFigure'
STB_SEC_BEAM_S, STB_SEC_STEEL_BEAM = 'StbSecBeam_S', 'StbSecSteelBeam'
STB_MEMBERS = 'StbMembers'


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

    def get_next_free_node_id(self):
        return self.get_max_id(STB_NODE) + 1

    def get_next_free_member_id(self):
        return self.get_max_member_id() + 1

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

    def get_node_coord(self, id):
        if self.stb:
            for n in self.stb.iter('StbNode'):
                if int(n.attrib['id']) == id:
                    return float(n.attrib['x']), float(n.attrib['y']), float(n.attrib['z'])

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
                res.append(d)  # エレメントを返す？
                # res.append(d.attrib)
        return res

    def print_elements(self, tag):
        print('*** ', tag, ' ***')
        res = []
        for d in self.stb.iter(tag):
            res.append(d)
        for i in res:
            print(i.attrib)

    def get_max_member_id(self):
        # XPath 機能
        members = self.stb.findall('./StbModel/StbMembers//*[@id]')
        ids = []
        if members:
            for d in members:
                ids.append(int(d.attrib['id']))
        return max(ids)

    def add_node(self, x=0, y=0, z=0, kind="ON_BEAM"):
        id = self.get_next_free_node_id()
        nodes = self.stb.find('./StbModel/StbNodes')
        node = ET.Element(STB_NODE, dict(id=str(id), x=str(x), y=str(y), z=str(z), kind=kind))
        nodes.append(node)
        return id

    def add_beam(self, n1_id, n2_id, name='NA', id_sec=0):
        id = self.get_next_free_member_id()
        beams = self.stb.find('./StbModel/StbMembers/StbBeams')
        beam = ET.Element(STB_BEAM,
                          dict(id=str(id), name=name, idNode_start=str(n1_id), idNode_end=str(n2_id), rotate="0",
                               id_section=str(id_sec), kind_structure="S", isFoundation="FALSE", offset="0",
                               level="-50",
                               offset_start_Z="-50", offset_end_Z="-50", condition_start="PIN", condition_end="PIN"))
        beams.append(beam)
        pass

    def get_min_max_coord(self):
        xc = []
        yc = []
        zc = []
        if self.stb:
            for n in self.stb.iter('StbNode'):
                xc.append(float(n.attrib['x']))
                yc.append(float(n.attrib['y']))
                zc.append(float(n.attrib['z']))
        return (min(xc), max(xc)), (min(yc), max(yc)), (min(zc), max(zc))

    def plot_grids(self, show=False):
        line_style = dict(color='k', linestyle='dashdot', linewidth=0.6)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ext = 2000
        (xmin, xmax), (ymin, ymax) = self.get_min_max_coord()[:2]
        x_grid_names = self.get_name_list(STB_X_AXIS)
        y_grid_names = self.get_name_list(STB_Y_AXIS)

        for gn in x_grid_names:
            xc = self.get_element_attribute(STB_X_AXIS, name=gn)[0]['distance']
            ax.add_line(ml.Line2D((xc, xc), (ymin - ext, ymax + ext), **line_style))
            ax.annotate(gn, xy=(xc, ymin - ext))
            ax.annotate(gn, xy=(xc, ymax + ext))

        for gn in y_grid_names:
            yc = self.get_element_attribute(STB_Y_AXIS, name=gn)[0]['distance']
            ax.add_line(ml.Line2D((xmin - ext, xmax + ext), (yc, yc), **line_style))
            ax.annotate(gn, xy=(xmin - ext, yc))
            ax.annotate(gn, xy=(xmax + ext, yc))

        # ax.grid(True, linestyle=':', lw=0.5)
        plt.axis('equal')
        if show:
            plt.show()

    def get_story_node_list(self, story=""):
        nodes = []
        if self.stb:
            for d in self.stb.iter('StbStory'):
                if d.attrib['name'] == story:
                    for n in d.iter('StbNodeid'):
                        nodes.append(int(n.attrib['id']))
        return nodes

    def get_axis_node_list(self, axis=''):
        nodes = []
        if self.stb:
            for d in self.stb.iter('StbX_Axis'):
                if d.attrib['name'] == axis:
                    for n in d.iter('StbNodeid'):
                        nodes.append(int(n.attrib['id']))
            for d in self.stb.iter('StbY_Axis'):
                if d.attrib['name'] == axis:
                    for n in d.iter('StbNodeid'):
                        nodes.append(int(n.attrib['id']))
        return nodes

    def plot_column(self, story='', show=False):
        ct_style = dict(color='c', linestyle='solid', linewidth=1, fill=False)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        nodes = self.get_story_node_list(story)
        for n in nodes:
            col = self.get_elements(STB_COLUMN, idNode_top=str(n))
            if col:
                x, y, z = self.get_node_coord(n)
                ax.add_patch(mp.Circle((x, y), radius=100, **ct_style))
        plt.axis('equal')
        if show:
            plt.show()
        pass
