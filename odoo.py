import xml.etree.ElementTree as ET


def main():
    tree = ET.parse('country_data.xml')
    parser = ET.XMLPullParser(['start', 'end'])
    parser.feed('<rank>sometext')
    root = tree.getroot()
    
    print(root.tag)
    print(root[0][1].text)
    for child in root:
        print(child.tag, child.attrib)
        print(root[2][0].text)
    
    for country in root.findall('country'):
        rank = country.find('rank').text
        name = country.get('name')
        print(name, rank)



if __name__ == "__main__":
    main()
