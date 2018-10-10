import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.lines as ml
import matplotlib.patches as mp
import math
import xml.dom.minidom as minidom

STB_NODE, STB_X_AXIS, STB_Y_AXIS, STB_STORY = 'StbNode', 'StbX_Axis', 'StbY_Axis', 'StbStory'
STB_COLUMN, STB_GIRDER, STB_BEAM, STB_BRACE = 'StbColumn', 'StbGirder', 'StbBeam', 'StbBrace'
STB_SEC_COLUMN_S, STB_SEC_STEEL_COLUMN = 'StbSecColumn_S', 'StbSecSteelColumn'
STB_SEC_BEAM_RC, STB_SEC_FIG = 'StbSecBeam_RC', 'StbSecFigure'
STB_SEC_BEAM_S, STB_SEC_STEEL_BEAM = 'StbSecBeam_S', 'StbSecSteelBeam'
STB_MEMBERS = 'StbMembers'


def mid_point(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def get_theta(p1, p2):
    """p1->p2の直線の、X軸からの傾き角度thetaを返す"""
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dy, dx)


def get_shortened_points(p1, p2, d=100):
    """
    はりの図形表示で、端部にジョイントを示す○を描くため
    端部座標を縮めた座標を計算する。
    :param p1:
    :param p2:
    :param d:
    :return:
    """
    theta = get_theta(p1, p2)
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x11 = x1 + d * math.cos(theta)
    y11 = y1 + d * math.sin(theta)
    x21 = x2 - d * math.cos(theta)
    y21 = y2 - d * math.sin(theta)
    # print((x11, y11), (x21, y21))
    return (x11, y11), (x21, y21)


class Stb:
    def __init__(self):
        self.stb = None

    def new_stb(self):
        """
        STBデータ新規作成 v.1.4
        """
        st = ET.Element('ST_BRIDGE')
        st.set('version', '1.4.00')

        mdl = ET.SubElement(st, 'StbModel')
        nodes = ET.SubElement(mdl, 'StbNodes')

        axes = ET.SubElement(mdl, 'StbAxes')
        stories = ET.SubElement(mdl, 'StbStories')
        members = ET.SubElement(mdl, 'StbMembers')
        columns = ET.SubElement(members, 'StbColumns')
        posts = ET.SubElement(members, 'StbPosts')
        girders = ET.SubElement(members, 'StbGirders')
        beams = ET.SubElement(members, 'StbBeams')
        braces = ET.SubElement(members, 'StbBraces')
        slabs = ET.SubElement(members, 'StbSlabs')
        walls = ET.SubElement(members, 'StbWalls')
        parapets = ET.SubElement(members, 'StbParapets')
        foudation_columns = ET.SubElement(members, 'StbFoundationColumns')
        footings = ET.SubElement(members, 'StbFootings')
        strip_footings = ET.SubElement(members, 'StbStrip_Footings')
        piles = ET.SubElement(members, 'StbPiles')
        sections = ET.SubElement(mdl, 'StbSections')
        sec_s = ET.SubElement(sections, 'StbSecSteel')
        joints = ET.SubElement(mdl, 'StbJoints')
        self.stb = ET.ElementTree(element=st).getroot()

    def load_stb(self, file):
        """
        ファイルSTBから読み込み
        """
        with open(file, 'r', encoding='Shift_JIS') as f:
            self.stb = ET.fromstring(f.read())

    def save_stb2(self, file):
        # new_stbとした場合の仮対応用
        txt = ET.tostring(self.stb, encoding='unicode')
        with open(file, 'w', encoding='Shift_JIS') as f:
            f.write('<?xml version="1.0" encoding="Shift_JIS"?>' + chr(10))
            f.write((minidom.parseString(txt)).toprettyxml(indent='  '))
            # f.write((minidom.parseString(txt)).toprettyxml(indent='  ',encoding='shift_jis'))

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
        """
        指定tag中のidを検索し、最大値を返す
        """
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

    def add_node(self, id=None, x=0, y=0, z=0, kind="OTHER"):
        if id is None:
            id = self.get_next_free_node_id()
        nodes = self.stb.find('./StbModel/StbNodes')
        node = ET.Element(STB_NODE, dict(id=str(id), x=str(x), y=str(y), z=str(z), kind=kind))
        nodes.append(node)
        return id

    def __add_node_tmp1(self):
        # 不要か
        # 通心生成のため、仮のNodeを作る
        # nodes = self.stb.find('./StbModel/StbNodes')
        # node = ET.Element(STB_NODE, dict(id=str(20000), x=str(0), y=str(0), z=str(0), kind='OTHER'))
        # nodes.append(node)
        pass

    def add_beam_tmp(self, n1_id, n2_id, name='NA', id_sec=0):
        # テスト用？
        id = self.get_next_free_member_id()
        beams = self.stb.find('./StbModel/StbMembers/StbBeams')
        beam = ET.Element(STB_BEAM,
                          dict(id=str(id), name=name, idNode_start=str(n1_id), idNode_end=str(n2_id), rotate="0",
                               level='0', id_section=str(id_sec), kind_structure="S", isFoundation="FALSE", offset="0",
                               condition_start="PIN", condition_end="PIN"))
        beams.append(beam)

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

    def plot_grids(self, ax):
        line_style = dict(color='k', linestyle='dashdot', linewidth=0.6)
        text_style = dict(color='k', size='small')
        ext = 2000
        (xmin, xmax), (ymin, ymax) = self.get_min_max_coord()[:2]
        x_grid_names = self.get_name_list(STB_X_AXIS)
        y_grid_names = self.get_name_list(STB_Y_AXIS)

        for gn in x_grid_names:
            xc = self.get_element_attribute(STB_X_AXIS, name=gn)[0]['distance']
            ax.add_line(ml.Line2D((xc, xc), (ymin - ext, ymax + ext), **line_style))
            ax.annotate(gn, xy=(xc, ymin - ext), **text_style)
            ax.annotate(gn, xy=(xc, ymax + ext), **text_style)

        for gn in y_grid_names:
            yc = self.get_element_attribute(STB_Y_AXIS, name=gn)[0]['distance']
            ax.add_line(ml.Line2D((xmin - ext, xmax + ext), (yc, yc), **line_style))
            ax.annotate(gn, xy=(xmin - ext, yc), **text_style)
            ax.annotate(gn, xy=(xmax + ext, yc), **text_style)

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

    def plot_column(self, ax, story, show_node_num=False, show_fugou=True):
        ct_style = dict(color='m', linestyle='solid', linewidth=2., fill=False)
        text_style = dict(textcoords='offset points', color='m', size='x-small')

        nodes = self.get_story_node_list(story)
        for n in nodes:
            col = self.get_elements(STB_COLUMN, idNode_top=str(n))
            if col:
                x, y, z = self.get_node_coord(n)
                ax.add_patch(mp.Circle((x, y), radius=75, **ct_style))
                # 節点番号
                if show_node_num:
                    ax.annotate(str(n), (x, y), xytext=(3, 3), **text_style)
                # 柱符号
                if show_fugou:
                    ax.annotate(col[0].attrib['name'], (x, y), xytext=(3, -9), **text_style)

    def plot_girder(self, ax, story, show_fugou=True):
        line_style = dict(color='g', linestyle='solid', linewidth=2., marker='.')
        text_style = dict(textcoords='offset points', color='g', size='x-small')

        nodes = self.get_story_node_list(story)
        for n in nodes:
            gir = self.get_elements(STB_GIRDER, idNode_start=str(n))
            if gir:
                for g in gir:  # 始点番号が同じで異なる梁がある
                    x1, y1, z1 = self.get_node_coord(n)
                    x2, y2, z2 = self.get_node_coord(int(g.attrib['idNode_end']))
                    p11, p21 = get_shortened_points((x1, y1), (x2, y2), 150)
                    # ax.add_line(ml.Line2D((x1, x2), (y1, y2), **line_style))
                    ax.add_line(ml.Line2D((p11[0], p21[0]), (p11[1], p21[1]), **line_style))
                    if show_fugou:
                        ax.annotate(g.attrib['name'], (mid_point((x1, y1), (x2, y2))), xytext=(1, 3), **text_style)

    def plot_beam(self, ax, story, show_fugou=True):
        line_style = dict(color='b', linestyle='solid', linewidth=2., marker='.')
        text_style = dict(textcoords='offset points', color='b', size='x-small')

        nodes = self.get_story_node_list(story)
        for n in nodes:
            gir = self.get_elements(STB_BEAM, idNode_start=str(n))
            if gir:
                for g in gir:  # 始点番号が同じで異なる梁がある
                    x1, y1, z1 = self.get_node_coord(n)
                    x2, y2, z2 = self.get_node_coord(int(g.attrib['idNode_end']))
                    p11, p21 = get_shortened_points((x1, y1), (x2, y2), 150)
                    # ax.add_line(ml.Line2D((x1, x2), (y1, y2), **line_style))
                    ax.add_line(ml.Line2D((p11[0], p21[0]), (p11[1], p21[1]), **line_style))
                    if show_fugou:
                        ax.annotate(g.attrib['name'], (mid_point((x1, y1), (x2, y2))), xytext=(1, 3), **text_style)

    def plot(self, grid=True, col=False, gir=False, beam=False, story=''):
        """伏せ図プロット"""
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        if grid:
            self.plot_grids(ax)
        if col:
            self.plot_column(ax, story)
        if gir:
            self.plot_girder(ax, story)
        if beam:
            self.plot_beam(ax, story)

        plt.axis('equal')
        plt.show()

    def add_grid(self, param, id, name, distance):
        # Gridを一つ生成する
        axes = self.stb.find('./StbModel/StbAxes')
        ax = ET.Element(param, dict(id=str(id), name=str(name), distance=str(distance)))
        node_list = ET.Element('StbNodeid_List')  # これがないと、Revit2017読み込みエラーとなる。
        node_id = ET.Element('StbNodeid', id='1')  # 試しに、すべてid=1としてみる。とりあえず、読み込める。

        node_list.append(node_id)
        ax.append(node_list)
        axes.append(ax)

    def add_story(self, id, name, height):
        """
        層を生成する
        :param id:
        :param name:
        :param height:
        :return:
        """
        # 層を生成する
        stories = self.stb.find('./StbModel/StbStories')
        node_list = ET.Element('StbNodeid_List')  # これがないと、Revit2017読み込みエラーとなる。
        st = ET.Element('StbStory', dict(id=str(id), name=str(name), height=str(height), kind='GENERAL'))
        st.append(node_list)
        stories.append(st)

    def add_story_test(self, id=0, name="", height=0):
        # テスト用　
        stories = self.stb.find('./StbModel/StbStories')
        node_list = ET.Element('StbNodeid_List')  # これがないと、Revit2017読み込みエラーとなる。

        st1 = ET.Element('StbStory', dict(id='1', name='1F', height='100', kind='GENERAL'))
        st1.append(node_list)
        st2 = ET.Element('StbStory', dict(id='2', name='RF', height='3000', kind='GENERAL'))
        st2.append(node_list)
        stories.append(st1)
        stories.append(st2)

    def add_column(self, id, fugou, b_node_id, t_node_id, sec_id, kind='S'):
        columns = self.stb.find('./StbModel/StbMembers/StbColumns')
        col = ET.Element(STB_COLUMN, dict(id=str(id), name=str(fugou), idNode_bottom=str(b_node_id),
                                          idNode_top=str(t_node_id), id_section=str(sec_id), kind_structure=str(kind)))
        columns.append(col)

    def add_girder(self, id, fugou, node1, node2, sec_id, kind='S'):
        girders = self.stb.find('./StbModel/StbMembers/StbGirders')
        gir = ET.Element(STB_GIRDER, dict(id=str(id)), name=str(fugou), idNode_start=str(node1), idNode_end=str(node2),
                         id_section=str(sec_id), kind_structure=str(kind))
        girders.append(gir)

    def add_beam(self,id,fugou,node1,node2,sec_id,kind='S',**kwargs):
        beams = self.stb.find('./StbModel/StbMembers/StbBeams')

        b = ET.Element(STB_BEAM,dict(id=str(id),name=str(fugou),idNode_start=str(node1),idNode_end=str(node2),
                                     id_section=str(sec_id),kind_structure=str(kind),**kwargs))
        beams.append(b)


    def add_col_test(self):
        # add section
        self.add_section_test()

        # add_node
        # nid1 = self.add_node(0, 0, 0, kind='OTHER')
        # nid2 = self.add_node(0, 0, 3000, kind='OTHER')
        nodes = self.stb.find('./StbModel/StbNodes')
        n1 = ET.Element(STB_NODE, dict(id=str(1), x=str(0), y=str(0), z=str(0), kind='OTHER'))
        n11 = ET.Element(STB_NODE, dict(id=str(2), x=str(0), y=str(0), z=str(3000), kind='OTHER'))
        nodes.append(n1)
        nodes.append(n11)

        cid = 1
        columns = self.stb.find('./StbModel/StbMembers/StbColumns')
        col = ET.Element(STB_COLUMN, dict(id=str(cid), idNode_bottom=str(1), idNode_top=str(2), id_section='1',
                                          kind_structure='S'))
        columns.append(col)

    def add_section_test(self):
        sections = self.stb.find('./StbModel/StbSections')
        sec_s = self.stb.find('./StbModel/StbSections/StbSecSteel')
        # sec_s = ET.Element('StbSecSteel')
        sec_sRB = ET.Element('StbSecRoll-BOX',
                             dict(name="□-125x125x3.2x6.4", type='STKR', A="125", B="125", t="3.2", R="6.4"))
        sec_s.append(sec_sRB)
        sections.append(sec_s)
        sec_col = ET.Element(STB_SEC_COLUMN_S, dict(id="1", name="C1", kind_column="COLUMN", direction="TRUE"))
        sec_col_s = ET.Element('StbSecSteelColumn', dict(pos="ALL", shape="□-125x125x3.2x6.4", strength_main="STKR400"))
        sec_col.append(sec_col_s)
        sections.append(sec_col)

    def add_section_steel_shape(self, sections):
        """
        StbSecSteel要素を追加する
        TODO:部材種別の追加
        :param sections:リスト
        :return:
        """
        sec_s = self.stb.find('./StbModel/StbSections/StbSecSteel')
        for sec in sections:
            if sec['name'][0] == '□':
                s = ET.Element('StbSecRoll-BOX',
                               dict(name=str(sec['name']), type='STKR', A=str(sec['A']), B=str(sec['B']),
                                    t=str(sec['t']), R=str(sec['r'])))
            elif sec['name'][0] == 'H':
                s = ET.Element('StbSecRoll-H',
                               dict(name=sec['name'], type='H', A=sec['A'], B=sec['B'], t1=sec['t1'], t2=sec['t2'],
                                    r=sec['r']))
            elif sec['name'][0] == 'C':
                s = ET.Element('StbSecRoll-LipC',
                               dict(name=sec['name'], type='C', H=sec['H'], A=sec['A'], C=sec['C'], t=sec['t']))

            elif sec['name'][:2] == '2C':  # 背中あわせとする
                s = ET.Element('StbSecRoll-LipC', dict(name=sec['name'], type='2C', H=sec['H'],
                                                       A=sec['A'], C=sec['C'], t=sec['t'], side='TRUE'))
            else:
                print(sec['name'])
            # append
            sec_s.append(s)

    def add_section(self, sections, type, kind_beam=None,sid_delta=0):
        stb_sec = self.stb.find('./StbModel/StbSections')
        sub_type = {'StbSecColumn_S': 'StbSecSteelColumn', 'StbSecBeam_S': 'StbSecSteelBeam'}
        # sid_delta = {'GIRDER': 1, 'BEAM': 101}
        for i, sec in enumerate(sections):
            if type == "StbSecColumn_S":
                s = ET.Element(type, dict(id=str(i + 1), name=sec['fugou']))
            elif type == 'StbSecBeam_S':
                s = ET.Element(type, dict(id=str(i + 1+sid_delta), name=sec['fugou'], kind_beam=kind_beam))
            if type == "StbSecColumn_S":
                s2 = ET.Element(sub_type[type], dict(pos='ALL', shape=sec['name']))
            elif type == 'StbSecBeam_S':
                s2 = ET.Element(sub_type[type], dict(pos='ALL', shape=sec['name']))

            s.append(s2)
            stb_sec.append(s)
