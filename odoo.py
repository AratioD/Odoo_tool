"""
2020-08-07 Demo software. @AratioD
"""
import time
import datetime
import re
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
        # Input validation
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
    # List for refined objects
    refined_objects = []

    for elem in fields_objects:
        # A creation of instance.
        ro = Model()
        found_match = False
        for elem1 in model_objects:
            if elem.data_model == elem1.data_model:
                found_match = True

        # Because no match found value is "_inherit"
        if found_match == True:
            ro.data_name_or_inherit = ("_name", "name")
        else:
            ro.data_name_or_inherit = ("_inherit", "name")

        ro.data_model = (elem.data_model[0], elem.data_model[1])
        ro.data_name = (elem.data_name[0], elem.data_name[1])
        ro.data_type = (elem.data_type[0], elem.data_type[1])
        refined_objects.append(ro)

    return refined_objects


def write_data(refined_objects, result_file_name):

    f = open(result_file_name, "a")

    # Imports to py file.
    row0 = (f'from odoo import models, fields')

    f.write(row0)
    f.write('\n')
    f.write('\n')

    for ro in refined_objects:
        row1 = (f'class AModel(models.Model):')
        row2 = (
            f'      {ro.data_name_or_inherit[0]} = a.{ro.data_model[0]}.{ro.data_name[0]}')
        row3 = (f'      field1 = fields.{ro.data_type[0]}()')

        f.write(row1)
        f.write('\n')
        f.write(row2)
        f.write('\n')
        f.write(row3)
        f.write('\n')
        f.write('\n')


def loop_ir_model():
    """
    Loop all specified model fields.
    The field is
    1. model
    Returns: Object_list full Model() instances.
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


def time_stamp_filename():
    timestamp = time.time()
    readable = datetime.datetime.fromtimestamp(timestamp).isoformat()
    timestamp = re.sub("[-:]", "_", readable)
    file_name = str(timestamp) + "_Odoo_.py"
    open(file_name, 'a').close()
    return file_name


def main():
    """
    Tha main class which calls all needed functions.
    Functions:
    1. The file function. Call a file function to generate a new python file.
    2. The field collect function. Loops and collect needed field data from the file.
    3. The model collect function. Concanate and refine model data and field data.
    4. The refine data function. Concanate and refine model data and field data
    5. The write refined data to file function.  Writes file from the refined list of objects.
    """
    # Call a file function to generate a new python file.
    result_file_name = time_stamp_filename()
    # Loops and collect needed field data from the file.
    fields_objects = loop_ir_model_fields()
    # Loops and collect needed field data from the file.
    model_objects = loop_ir_model()
    # Concanate and refine model data and field data
    refined_objects = refine_data(fields_objects, model_objects)
    # Writes file from the refined list of objects.
    write_data(refined_objects, result_file_name)


if __name__ == "__main__":
    main()
