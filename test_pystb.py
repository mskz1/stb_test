from pystb import Stb, STB_NODE, STB_X_AXIS
import pytest
from pytest import approx


@pytest.fixture
def stb():
    filename = 'test.STB'
    st = Stb()
    st.load_stb(filename)
    return st


def test_node_max(stb):
    assert stb.get_max_node_id() == 382
    assert stb.get_node_numbers() == 148


def test_node_coordinates(stb):
    assert stb.get_node_x(id=5) == approx(7200)
    assert stb.get_node_y(id=5) == approx(0)
    assert stb.get_node_z(id=5) == approx(150)
    assert stb.get_node_x(id=104) == approx(21600)
    assert stb.get_node_y(id=104) == approx(12600)
    assert stb.get_node_z(id=350) == approx(4350)
    assert stb.get_node_x(id=93) is None


def test_axis_names(stb):
    assert stb.get_x_axis_names() == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    assert stb.get_y_axis_names() == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


def test_axis_coordinates(stb):
    assert stb.get_x_axis_distance('3') == approx(3600)
    assert stb.get_y_axis_distance('G') == approx(10800)


def test_story_names(stb):
    assert stb.get_story_names() == ['1F', 'MF', 'RF']


def test_story_height(stb):
    assert stb.get_story_height('RF') == approx(4350)


def test_column_max(stb):
    assert stb.get_max_column_id() == 82
    assert stb.get_column_numbers() == 82


def test_get_element_data(stb):
    assert stb.get_element_attribute(STB_NODE, id='6') == {'id': '6', 'x': '9000', 'y': '0', 'z': '150',
                                                           'kind': 'ON_GRID'}


def test_get_elements(stb):
    li = stb.get_elements(STB_NODE, y='0', z='150')
    for i in li:
        print(i)
