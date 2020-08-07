import xml.etree.ElementTree as ET


class ValidString:
    """
    The class ValidString validates all string based values in the module.
    Numerical values are not allowed and strings validation rules are
    1. If "ttype" capitalize a first letter.
    2. If data type is "name" and string starts with "x_". Cut the "x_ value"
    3. If data type is "model". No modifications. 
    """

    def __init__(self, min_lenght=None):
        self.min_lenght = min_lenght

    def __set_name__(self, owner_class, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        # Unpack the actual value and value type.
        value, value_type = value
        if not isinstance(value, str):
            raise ValueError(f'ERROR! {self.property_name} MUST BE A STRING!')
        if self.min_lenght is not None and len(value) < self.min_lenght:
            raise ValueError(
                f'ERROR! {self.property_name} MUST BE AT LEAST {self.min_lenght} CHARACTERS!'
            )

        if value_type == "ttype":
            temp = value.capitalize()
            instance.__dict__[self.property_name] = temp
        elif value_type == "name":
            if "x_" == value[0:2]:
                temp = value[2:]
                instance.__dict__[self.property_name] = temp
            else:
                instance.__dict__[self.property_name] = value
        elif value_type == "model":
            instance.__dict__[self.property_name] = value

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name, None)


class Model:
    data_type = ValidString(2)
    data_name = ValidString(2)
    data_model = ValidString(2)


def loop_ir_model_fields():

    tree = ET.parse('ir_model_fields.xml')
    root = tree.getroot()
    # # print(root.tag)
    # # print(root[0][1].text)
    object_list = []
    for child in root:
        # print(child.tag, child.attrib)
        # print(root[0][0].text)
        p = Model()

        for cc in child:
            tag_type = cc.get('name')
            if tag_type == "model":
                p.data_model = (cc.text, tag_type)
            elif tag_type == "name":
                p.data_name = (cc.text, tag_type)
            elif tag_type == "ttype":
                p.data_type = (cc.text, tag_type)

        object_list.append(p)

    return object_list


def main():
    """
    Tha main class which calls all needed functions.
    """

    objects = loop_ir_model_fields()

    for dd in objects:
        print("model--> ", dd.data_model, " <--name-->",
              dd.data_name, "<--type-->", dd.data_type)
        # print(dd.data_type)


if __name__ == "__main__":
    main()
