import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def test_et():
    # st = ET.Element('ST_BRIDGE', version="1.4.00")
    st = ET.Element('ST_BRIDGE')
    st.set('version', '1.4.00')

    mdl = ET.SubElement(st, 'StbModel')
    axes = ET.SubElement(mdl, 'StbAxes')
    x1 = ET.SubElement(axes, 'StbX_Axis')
    x1.set('id', '1')
    x1.set('name', '1')
    x1.set('distance', '0')
    tree = ET.ElementTree(element=st)

    # ET.dump(tree)

    string = ET.tostring(tree.getroot(), 'utf-8')
    pretty_string = minidom.parseString(string).toprettyxml(indent='  ')
    print(pretty_string)


def xtest_2():
    root = ET.Element('root')

    sub = ET.SubElement(root, 'sub')

    subsub = ET.SubElement(sub, 'subsub')
    subsub.set('key', 'value')
    subsub.text = 'text'

    subsub2 = ET.SubElement(sub, 'subsub2')
    subsub2.set('key2', 'あvalue2日本語')
    subsub2.text = 'あtext2'

    tree = ET.ElementTree(element=root)
    ET.dump(tree)
