from pystb import Stb, STB_NODE, STB_X_AXIS, STB_Y_AXIS, STB_STORY, STB_COLUMN, STB_GIRDER, STB_BEAM, STB_BRACE
from pystb import STB_SEC_COLUMN_S, STB_SEC_STEEL_COLUMN
from pystb import STB_SEC_BEAM_S, STB_SEC_STEEL_BEAM
from pystb import STB_MEMBERS
import pytest
from pytest import approx
from pystb import mid_point, get_theta, get_shortened_points
import math


@pytest.fixture
def stb():
    filename = 'test.STB'
    st = Stb()
    st.load_stb(filename)
    return st


def test_node_max(stb):
    assert stb.get_max_id(STB_NODE) == 382
    assert stb.get_node_numbers() == 148
    # StbMembers の max_id
    assert stb.get_max_member_id() == 299


def test_node_coordinates(stb):
    # assert stb.get_node_x(id=5) == approx(7200)
    assert stb.get_element_attribute(STB_NODE, id='5')[0]['x'] == '7200'
    # assert stb.get_node_y(id=5) == approx(0)
    assert stb.get_element_attribute(STB_NODE, id='5')[0]['y'] == '0'
    # assert stb.get_node_z(id=5) == approx(150)
    assert stb.get_element_attribute(STB_NODE, id='5')[0]['z'] == '150'
    # assert stb.get_node_x(id=104) == approx(21600)
    assert stb.get_element_attribute(STB_NODE, id='104')[0]['x'] == '21600'
    # assert stb.get_node_y(id=104) == approx(12600)
    assert stb.get_element_attribute(STB_NODE, id='104')[0]['y'] == '12600'
    # assert stb.get_node_z(id=350) == approx(4350)
    assert stb.get_element_attribute(STB_NODE, id='350')[0]['z'] == '4350'
    assert stb.get_node_x(id=93) is None
    # 該当データがない場合 [] が返る
    assert stb.get_element_attribute(STB_NODE, id='93') == []


def test_name_list(stb):
    assert stb.get_name_list(STB_X_AXIS) == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    assert stb.get_name_list(STB_Y_AXIS) == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    assert stb.get_name_list(STB_STORY) == ['1F', 'MF', 'RF']


def test_axis_coordinates(stb):
    # assert stb.get_x_axis_distance('3') == approx(3600)
    assert stb.get_element_attribute(STB_X_AXIS, name='3')[0]['distance'] == '3600'
    # assert stb.get_y_axis_distance('G') == approx(10800)
    assert stb.get_element_attribute(STB_Y_AXIS, name='G')[0]['distance'] == '10800'


def test_story_height(stb):
    # assert stb.get_story_height('RF') == approx(4350)
    assert stb.get_element_attribute(STB_STORY, name='RF')[0]['height'] == '4350'


def test_column_max(stb):
    assert stb.get_max_id(STB_COLUMN) == 82
    assert stb.get_column_numbers() == 82


def test_get_elements(stb):
    # li = stb.get_element_attribute(STB_NODE, y='0', z='150')
    # for i in li:
    #     print(i)
    # li = stb.get_element_attribute(STB_COLUMN, name='C3')
    # for i in li:
    #     print(i)
    # print()
    # print('col_shape------')
    # li = stb.get_element_attribute(STB_SEC_STEEL_COLUMN)
    # for i in li:
    #     print(i)
    # print('beam_shape------')
    # li = stb.get_element_attribute(STB_SEC_STEEL_BEAM)
    # for i in li:
    #     print(i)

    assert stb.get_element_attribute(STB_NODE, id='6')[0] == {'id': '6', 'x': '9000', 'y': '0', 'z': '150',
                                                              'kind': 'ON_GRID'}
    assert len(stb.get_element_attribute(STB_NODE)) == 148
    assert stb.get_element_attribute(STB_COLUMN, id='1')[0] == {'id': '1', 'name': 'C3', 'idNode_bottom': '1',
                                                                'idNode_top': '118', 'rotate': '0', 'id_section': '1',
                                                                'kind_structure': 'S', 'offset_X': '0', 'offset_Y': '0',
                                                                'offset_bottom_Z': '-1050', 'condition_bottom': 'FIX'}


def test_save_stb(stb):
    o_file_name = 'output_save_test.stb'
    stb.save_stb(o_file_name)
    pass


def test_show_elements(stb):
    # stb.print_elements(STB_X_AXIS)
    # stb.print_elements(STB_STORY)
    # stb.print_elements(STB_SEC_STEEL_COLUMN)
    # stb.print_elements(STB_SEC_STEEL_BEAM)
    # stb.print_elements(STB_COLUMN)
    pass


def test_element_modify(stb):
    # stb.print_elements(STB_STORY)
    elems = stb.get_elements(STB_STORY, name='RF')
    e = elems[0]
    e.attrib['height'] = '5000'
    # stb.print_elements(STB_STORY)
    elems = stb.get_element_attribute(STB_STORY, name='RF')
    assert elems[0]['height'] == '5000'


def test_add_node(stb):
    assert stb.get_max_id(STB_NODE) == 382
    assert stb.get_next_free_node_id() == 383
    stb.add_node(x=100, y=100, z=300)
    assert stb.get_max_id(STB_NODE) == 383
    pass


def test_add_beam(stb):
    # stb.print_elements(STB_BEAM)
    n1_id = stb.add_node(x=0, y=0, z=1000)
    n2_id = stb.add_node(x=2000, y=0, z=1000)
    stb.add_beam(n1_id, n2_id, name='V1A', id_sec=18)
    # stb.print_elements(STB_BEAM)
    pass


def test_min_max_coord_of_node(stb):
    # print(stb.get_min_max_coord())
    assert (stb.get_min_max_coord() == ((0.0, 21600.0), (0.0, 14400.0), (150.0, 4350.0)))


def test_plot_grid_line(stb):
    # stb.plot(col=False)
    pass


def test_get_story_nodes(stb):
    assert stb.get_story_node_list("1F") == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 26, 27, 39, 40, 52, 53, 58,
                                             62, 65, 66, 78, 79, 91, 92, 104, 105, 106, 107, 109, 110, 111, 112, 113,
                                             114, 115, 116, 117]


def test_get_axis_nodes(stb):
    assert stb.get_axis_node_list('A') == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 118, 119, 120, 121, 122, 123, 124,
                                           125, 126, 127, 128, 129, 130, 235, 236, 237, 238, 239, 240, 241, 242, 243,
                                           244, 245, 246, 247]


def test_plot_column(stb):
    # stb.plot(col=True, gir=True, beam=True, story='RF')
    # stb.plot(grid=False, col=True, gir=True, beam=True, story='RF')

    # stb.plot(col=True, gir=True, story='MF')
    # stb.plot(col=True, gir=True, story='1F')
    pass


def test_mid_point():
    assert mid_point((0, 0), (6, 4)) == (3, 2)


def test_theta():
    assert get_theta((0, 0), (1, 1)) == approx(math.pi / 4)
    assert get_theta((0, 0), (1, 1)) == approx(math.radians(45))
    assert get_theta((0, 0), (1, math.sqrt(3))) == approx(math.radians(60))
    assert get_theta((0, 0), (1, -1)) == approx(-math.pi / 4)
    assert get_theta((0, 0), (-1, 1)) == approx(3 * math.pi / 4)
    assert get_theta((0, 0), (-1, -1)) == approx(-3 * math.pi / 4)


def test_modify_line_end_point():
    assert get_shortened_points((0, 0), (4000, 0), 100) == ((100, 0), (3900, 0))
    assert get_shortened_points((0, 0), (-4000, 0), 100) == ((approx(-100), approx(0)), (approx(-3900), approx(0)))
    assert get_shortened_points((0, 0), (0, 3000), 200) == ((approx(0), approx(200)), (approx(0), approx(2800)))
    assert get_shortened_points((0, -3000), (0, 3000), 200) == ((approx(0), approx(-2800)), (approx(0), approx(2800)))
    assert get_shortened_points((0, 0), (2000, 2000), 100) == (
        (approx(70.7107), approx(70.7107)), (approx(1929.289), approx(1929.289)))


def test_new_stb():
    # import xml.etree.ElementTree as ET
    # st = ET.Element('ST_BRIDGE')
    # st.set('version', '1.4.00')
    #
    # mdl = ET.SubElement(st, 'StbModel')
    # axes = ET.SubElement(mdl, 'StbAxes')
    # x1 = ET.SubElement(axes, 'StbX_Axis')
    # x1.set('id', '1')
    # x1.set('name', '1')
    # x1.set('distance', '0')
    # tree = ET.ElementTree(element=st)

    ss = Stb()
    # ss.stb = ET.ElementTree(element=st).getroot()
    ss.new_stb()
    ss.save_stb2("output_new.stb")
    pass


def test_new_stb_grid():
    ss = Stb()
    ss.new_stb()
    ss.add_grid(STB_X_AXIS, id=1, name=1, distance=0)
    ss.add_grid(STB_X_AXIS, id=2, name=2, distance=5000.)
    ss.add_grid(STB_X_AXIS, id=3, name=3, distance=10000.)
    ss.add_grid(STB_Y_AXIS, id=101, name='A', distance=0)
    ss.add_grid(STB_Y_AXIS, id=102, name='B', distance=8000.)

    ss.save_stb2('output_new_grid.stb')
    pass
