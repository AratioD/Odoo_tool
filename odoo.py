import xml.etree.ElementTree as ET

def main():
    tree = ET.parse('ir_model_fields.xml')
    root = tree.getroot()
    
    # # print(root.tag)
    # # print(root[0][1].text)
    for child in root:
        # print(child.tag, child.attrib)
        # print(root[0][0].text)
        for cc in child:
            #  print(cc.tag, cc.attrib)
            rank = cc.get('name')
            if rank == "field_description":
                # rank2 = cc.get(rank)
                print("kissa -->", cc.get('name'))
                tett = child.find('field')
                print("kissa -->", tett.text)

    # for country in root.findall('field'):
    #     # print(country.getchildren)
    #     rank = country.find('field').text
    #     # rank1 = country.find('year').text
    #     # rank2 = country.find('gdppc').text
    #     # name = country.get('name')
    #     print(rank)


if __name__ == "__main__":
    main()
