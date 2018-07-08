from pystb import Stb, STB_NODE, STB_X_AXIS, STB_Y_AXIS, STB_STORY, STB_COLUMN, STB_GIRDER, STB_BEAM, STB_BRACE
from pystb import STB_SEC_COLUMN_S, STB_SEC_STEEL_COLUMN
from pystb import STB_SEC_BEAM_S, STB_SEC_STEEL_BEAM
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


def test_node_coordinates(stb):
    assert stb.get_node_x(id=5) == approx(7200)
    assert stb.get_element_attribute(STB_NODE, id='5')[0]['x'] == '7200'
    assert stb.get_node_y(id=5) == approx(0)
    assert stb.get_element_attribute(STB_NODE, id='5')[0]['y'] == '0'
    assert stb.get_node_z(id=5) == approx(150)
    assert stb.get_element_attribute(STB_NODE, id='5')[0]['z'] == '150'
    assert stb.get_node_x(id=104) == approx(21600)
    assert stb.get_node_y(id=104) == approx(12600)
    assert stb.get_node_z(id=350) == approx(4350)
    assert stb.get_node_x(id=93) is None


def test_name_list(stb):
    assert stb.get_name_list(STB_X_AXIS) == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    assert stb.get_name_list(STB_Y_AXIS) == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    assert stb.get_name_list(STB_STORY) == ['1F', 'MF', 'RF']


def test_axis_coordinates(stb):
    assert stb.get_x_axis_distance('3') == approx(3600)
    assert stb.get_element_attribute(STB_X_AXIS, name='3')[0]['distance'] == '3600'
    assert stb.get_y_axis_distance('G') == approx(10800)


def test_story_height(stb):
    assert stb.get_story_height('RF') == approx(4350)


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
    print()
    print('col_shape------')
    li = stb.get_element_attribute(STB_SEC_STEEL_COLUMN)
    for i in li:
        print(i)
    print('beam_shape------')
    li = stb.get_element_attribute(STB_SEC_STEEL_BEAM)
    for i in li:
        print(i)

    assert stb.get_element_attribute(STB_NODE, id='6')[0] == {'id': '6', 'x': '9000', 'y': '0', 'z': '150',
                                                              'kind': 'ON_GRID'}
    assert len(stb.get_element_attribute(STB_NODE)) == 148
    assert stb.get_element_attribute(STB_COLUMN, id='1')[0] == {'id': '1', 'name': 'C3', 'idNode_bottom': '1',
                                                                'idNode_top': '118', 'rotate': '0', 'id_section': '1',
                                                                'kind_structure': 'S', 'offset_X': '0', 'offset_Y': '0',
                                                                'offset_bottom_Z': '-1050', 'condition_bottom': 'FIX'}
