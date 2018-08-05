from pystb import Stb, STB_NODE, STB_X_AXIS, STB_Y_AXIS, STB_STORY, STB_COLUMN, STB_GIRDER, STB_BEAM, STB_BRACE
from pystb import STB_SEC_COLUMN_S, STB_SEC_STEEL_COLUMN
from pystb import STB_SEC_BEAM_S, STB_SEC_STEEL_BEAM
from pystb import STB_MEMBERS
import pytest
from pytest import approx


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
    stb.print_elements(STB_BEAM)
    n1_id = stb.add_node(x=0, y=0, z=1000)
    n2_id = stb.add_node(x=2000, y=0, z=1000)
    stb.add_beam(n1_id, n2_id, name='V1A',id_sec=18)
    stb.print_elements(STB_BEAM)

    pass
