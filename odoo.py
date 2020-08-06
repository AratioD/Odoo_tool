import xml.etree.ElementTree as ET


class ValidString:
    """
    The class ValidString validates all string based values in the module. 
    Numerical values are not allowed and string needs to have a prober length, which user defines.
    """
    
    def __init__(self, min_lenght=None):
        self.min_lenght = min_lenght

    def __set_name__(self, owner_class, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f'ERROR! {self.property_name} MUST BE A STRING!')
        if self.min_lenght is not None and len(value) < self.min_lenght:
            raise ValueError(
                f'ERROR! {self.property_name} MUST BE AT LEAST {self.min_lenght} CHARACTERS!'
            )
        instance.__dict__[self.property_name] = value

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name, None)


class Model:
    ttype = ValidString(2)
    name = ValidString(2)
    model = ValidString(2)


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
    """
    Tha main class which calls all needed functions.
    """
    loop_ir_model_fields()


if __name__ == "__main__":
    main()
