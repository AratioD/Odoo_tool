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
            instance.__dict__[self.property_name] = (temp, value_type)
        elif value_type == "name":
            if "x_" == value[0:2]:
                temp = value[2:]
                instance.__dict__[self.property_name] = (temp, value_type)
            else:
                instance.__dict__[self.property_name] = (value, value_type)
        elif value_type == "model":
            instance.__dict__[self.property_name] = (value, value_type)

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name, None)


class Model:
    data_type = ValidString(2)
    data_name = ValidString(2)
    data_model = ValidString(2)
    data_name_or_inherit = ValidString(2)


def loop_ir_model_fields():
    """
    Loop all specified ir model fields.
    The fields are
    1. model
    2. name
    3. ttype
    """
    # Specified file name.
    tree = ET.parse('ir_model_fields.xml')
    root = tree.getroot()

    # Empty object list to be returned.
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


def refine_data(fields_objects, model_objects):
    """
    The function takes two parameters in and returns refined list.
    Parameters are.
    1. fields_objects
    2. model_objects
    """

    refined_objects = []
    ro = Model()
    for elem in fields_objects:
        for elem1 in model_objects:
            if elem.data_model == elem1.data_model:
                # Because a match found value is "_name"
                ro.data_name_or_inherit = ("_name", "name")
                ro.data_model = (elem.data_model[0], elem.data_model[1])
                ro.data_name = (elem.data_name[0], elem.data_name[1])
                ro.data_type = (elem.data_type[0], elem.data_type[1])
                refined_objects.append(ro)

                break
        # Because no match found value is "_inherit"
        ro.data_name_or_inherit = ("_inherit", "name")
        ro.data_model = (elem.data_model[0], elem.data_model[1])
        ro.data_name = (elem.data_name[0], elem.data_name[1])
        ro.data_type = (elem.data_type[0], elem.data_type[1])
        refined_objects.append(ro)

    return refined_objects

    # print("model--> ", dd.data_model, " <--name-->",
    #       dd.data_name, "<--type-->", dd.data_type)
    # print(dd.data_type)

    # for dd in model_objects:
    #     print("model--> ", dd.data_model)
    #     # print(dd.data_type)

    # import_str = "from odoo import models, fields"
    # import_class = "class AModel(models.Model):"
    # import_name = "        _name = 'a.model.name'"
    # import_field = "        field1 = fields.Char()"

    # print(import_str)
    # print()
    # print()
    # print()

    # for x in range(5):

    #     print(import_class)
    #     print()
    #     print(import_name)
    #     print()
    #     print(import_field)
    #     print()
    #     x = x+1


# from odoo import models, fields
# class AModel(models.Model):
#     _name = 'a.model.name'

#     field1 = fields.Char()

def loop_ir_model():
    """
    Loop all specified model fields.
    The field is
    1. model
    """
    # Specified file name.
    tree = ET.parse('ir_model.xml')
    root = tree.getroot()

    # Empty object list to be returned.
    object_list = []
    for child in root:
        p = Model()
        for cc in child:
            tag_type = cc.get('name')
            if tag_type == "model":
                p.data_model = (cc.text, tag_type)
        object_list.append(p)
    return object_list


def main():
    """
    Tha main class which calls all needed functions.
    """

    fields_objects = loop_ir_model_fields()
    model_objects = loop_ir_model()
    refined_objects = refine_data(fields_objects, model_objects)

    for xx in refined_objects:
        print(xx.data_model[1], "-->", xx.data_model[0], "|--", xx.data_name[1], "-->", xx.data_name[0],
              "|--", xx.data_type[1], "-->", xx.data_type[0], "|--",  xx.data_name_or_inherit[1], "-->", xx.data_name_or_inherit[0])

    # # for dd in fields_objects:

    # #     print("model--> ", dd.data_model, " <--name-->",
    # #           dd.data_name, "<--type-->", dd.data_type)
    # #     # print(dd.data_type)

    # for dd in model_objects:
    #     print("model--> ", dd.data_model)
    #     # print(dd.data_type)


if __name__ == "__main__":
    main()
