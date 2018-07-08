import xml.etree.ElementTree as ET

# xmlp = ET.XMLParser(encoding="Shift_JIS")
# stb = ET.parse('test.STB',parser=xmlp)

with open('test.STB', 'r', encoding='Shift_JIS') as f:
    stb = ET.fromstring(f.read())

print(stb)
print(stb.tag)
print(stb.attrib)
for child in stb:
    print(child.tag, child.attrib)
print('-' * 20)
mdl = stb[1]
for ch in mdl:
    print(ch.tag, ch.attrib)

print('-' * 20)
# ------
# 節点データ
for n in stb.iter('StbNode'):
    # print(type(n))  # <class 'xml.etree.ElementTree.Element'>
    print(n.tag, n.attrib)


# X軸データ
for gx in stb.iter('StbX_Axis'):
    print(gx.tag, gx.attrib)

# Y軸データ
for gy in stb.iter('StbY_Axis'):
    print(gy.tag, gy.attrib)

# 層データ
for s in stb.iter('StbStory'):
    print(s.tag, s.attrib)

# 柱データ
for c in stb.iter('StbColumn'):
    print(c.tag, c.attrib)

# 梁データ
for g in stb.iter('StbGirder'):
    print(g.tag, g.attrib)

# 小梁データ
for b in stb.iter('StbBeam'):
    print(b.tag, b.attrib)

# ブレースデータ
for br in stb.iter('StbBrace'):
    print(br.tag, br.attrib)

# スラブデータ
for sb in stb.iter('StbSlab'):
    print(sb.tag, sb.attrib)

# S柱断面データ
for scsc in stb.iter('StbSecColumn_S'):
    print(scsc.tag, scsc.attrib)
    for d in scsc.iter('StbSecSteelColumn'):
        print(d.tag, d.attrib)

# RC梁断面データ
for scrb in stb.iter('StbSecBeam_RC'):
    print(scrb.tag, scrb.attrib)
    for d in scrb.iter('StbSecFigure'):
        print(d.tag, d.attrib)

# S梁断面データ
for scsb in stb.iter('StbSecBeam_S'):
    print(scsb.tag, scsb.attrib)
    for d in scsb.iter('StbSecSteelBeam'):
        print(d.tag, d.attrib)

print('-'*30)
print('-----StbSecSteelColumn')
for d in stb.findall('.//StbSecSteelColumn'):
    print(d.tag,d.attrib)
print('-----StbSecFigure')
for d in stb.findall('.//StbSecFigure'):
    print(d.tag,d.attrib)

print('-----StbSecSteelBeam')
for d in stb.findall('.//StbSecSteelBeam'):
    print(d.tag,d.attrib)
