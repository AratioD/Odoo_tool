import xml.etree.ElementTree as ET


class ValidString:
    """
    The class Data validates all string based values in the module. 
    Numerical values are not allowed.
    """

    def __set_name__(self, owner_class, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(
                f'ERROR!--> {self.property_name} VALUE MUST BE AN INTEGER!')
        if value < 0:
            raise ValueError(
                f'ERROR!--> {self.property_name} VALUE NEEDS TO BE POSITIVE INTEGER!'
            )
        instance.__dict__[self.property_name] = value

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name, None)


class Model:
    ttype = Data()
    name = Data()
    model = Data()


def loop_ir_model_fields():
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


def main():
    loop_ir_model_fields()


if __name__ == "__main__":
    main()
