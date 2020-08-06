from xml.dom import minidom

# parse an xml file by name
mydoc = minidom.parse('ir_model_fields.xml')

items = mydoc.getElementsByTagName('field')

# # one specific item attribute
# print('Item #2 attribute:')
# print(items[1].attributes['field'].value)

# all item attributes
print('\nAll attributes:')
for elem in items:
    # print(elem.attributes['name'].value)
    if elem.attributes['name'].value == "field_description":
        print("works", elem.attributes['name'].value)

# # one specific item's data
# print('\nItem #2 data:')
# print(items[1].firstChild.data)
# print(items[1].childNodes[0].data)

# # all items data
# print('\nAll item data:')
# for elem in items:
#     print(elem.firstChild.data)