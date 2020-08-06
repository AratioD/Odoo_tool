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

            rank = cc.get('name')

            if rank == "field_description":
               print(cc.text)


if __name__ == "__main__":
    main()
