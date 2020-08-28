"""
2020-08-28 Demo software. @AratioD
"""
import time
import os
import datetime
import copy
import re
from xml.etree import ElementTree
from collections import defaultdict

class ValidString:
    """
    The class ValidString validates all string based values in the module.
    Numerical values are not allowed and string validation rules are.
    1. If "ttype" capitalize a first letter.
    2. If data type is "name" and string starts with "x_". Cut the "x_ value"
    3. If data type is "model". No modifications.
    4. If data type is "field_description". No modifications.
    Please note that descriptor also uses instances type!
    """

    def __init__(self, min_lenght=None):
        self.min_lenght = min_lenght

    def __set_name__(self, owner_class, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        # Unpack value and value type.
        value, value_type = value
        if not isinstance(value, str):
            raise ValueError(
                f'ERROR! {self.property_name} MUST BE A STRING! NOW IT IS --> {value}')
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
        elif value_type == "model" or value_type == "field_description":
            instance.__dict__[self.property_name] = (value, value_type)

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name, None)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.property_name == other.property_name)
        else:
            return NotImplemented


class Model:
    """
    A instance attribute can handle only string "str" data type.
    Class instances are Number inside parenthesis define the lenght of the string.
    1. data_model = ValidString(1)
    """
    data_model = ValidString(1)


class Field:
    """
    All instance attributes can handle only string "str" data types.
    Class instances are Number inside parenthesis define the lenght of the string.
    1. data_type = ValidString(1)
    2. data_name = ValidString(1)
    3. data_desc = ValidString(0)
    """
    data_type = ValidString(1)
    data_name = ValidString(1)
    data_desc = ValidString(0)


def loop_fields(file_name, Class):
    """
    Keyword arguments:
    Class -- takes an input Model() or Field() class.
    file_name -- takes input file location.
    Parameters
    The fields are
    1. name
    2. ttype
    3. field description
    Returns: A object_set full Model() instances.
    """
    # Dictionary which will be returned.
    object_dict = defaultdict(set)

    full_file = os.path.abspath(os.path.join(file_name))
    dom = ElementTree.parse(full_file)
    # Collect all <record> blocks.
    records = dom.findall('record')

    for c in records:

        p = Class()
        elem0 = c.find('.//field[@name="model"]')

        if elem0 is not None and elem0.text not in object_dict.keys():
            # A key set.
            object_set = set()
            # Create a key in the dictionary.
            object_dict[elem0.text]

            # Loop only if the class is Field()
            if Class is Field:

                elem1 = c.find('.//field[@name="name"]')
                if elem1 is not None:
                    p.data_name = (elem1.text, "name")

                elem2 = c.find('.//field[@name="ttype"]')
                if elem2 is not None:
                    p.data_type = (elem2.text, "ttype")

                elem3 = c.find('.//field[@name="field_description"]')
                if elem3 is not None:
                    p.data_desc = (elem3.text, "field_description")

            # Add a created instance into object set list
            object_set.add(p)
            # Assign a set to created key.
            object_dict[elem0.text] = object_set

        elif elem0 is not None and elem0.text in object_dict.keys():

            object_copy = set()
            object_copy = object_dict[elem0.text].copy()

            # Loop only if the class is Field()
            if Class is Field:
                elem1 = c.find('.//field[@name="name"]')
                if elem1 is not None:
                    p.data_name = (elem1.text, "name")

                elem2 = c.find('.//field[@name="ttype"]')
                if elem2 is not None:
                    p.data_type = (elem2.text, "ttype")

                elem3 = c.find('.//field[@name="field_description"]')
                if elem3 is not None:
                    p.data_desc = (elem3.text, "field_description")

            # Add a created instance into object set list
            object_copy.add(p)
            # Assign a set to created key.
            object_dict[elem0.text] = object_copy

    return object_dict


def refine_model(elem):
    """
    The function is callable from the function write_rows.
    """
    class_name = ""
    if "." in elem:
        class_name = elem.split(".")
        class_name = class_name[1].capitalize()
    elif "_" in elem:
        class_name = elem.split("_")
        class_name = class_name[0] + class_name[1]
        class_name = class_name.capitalize()
    else:
        class_name = elem
        class_name = class_name[1].capitalize()
    return class_name


def write_data(field_objects, model_objects, result_file_name):
    """
    Writes refined objects to time stamped file name
    Returns: Time-stamped Python file.
    Write loop is:
    1. empty models
    2. inherit_models
    3. name_models
    ****
    The function write_rows is for inherit_models and name_models.
    """

    f = open(result_file_name, "a")

    # Imports to py file.
    row0 = (f'from odoo import models, fields')

    f.write(row0)
    f.write('\n')
    f.write('\n')

    all_models = set()
    for k in field_objects.keys():
        all_models.add(k)

    for k in model_objects.keys():
        all_models.add(k)

    for models in all_models:
        if models not in field_objects.keys() and models in model_objects.keys():
            inherit = "_inherit"
            write_rows(models, f, inherit, field_objects)
        elif models in field_objects.keys() and models not in model_objects.keys():
            inherit = "_inherit"
            write_rows(models, f, inherit, field_objects)
        elif models in field_objects.keys() and models in model_objects.keys():
            inherit = "_name"
            write_rows(models, f, inherit, field_objects)


def write_rows(models, f, inherit, objects):
    class_name = refine_model(models)
    row1 = (f'class {class_name}(models.Model):')
    f.write('\n')
    f.write(row1)
    f.write('\n')
    row2 = (f'      {inherit} = \'{models}\'')
    f.write(row2)
    f.write('\n')

    values = objects[models]

    for ii in values:
        row3 = (
            f'      {ii.data_name[0]} = fields.{ii.data_type[0]}(string="{ii.data_desc[0]}")')
        f.write(row3)
        f.write('\n')


def time_stamp_filename():
    """
    The Function creates a new python file and generates a time stamp for that.
    Return: a file name
    """
    timestamp = time.time()
    readable = datetime.datetime.fromtimestamp(timestamp).isoformat()
    timestamp = re.sub("[-:]", "_", readable)
    file_name = str(timestamp) + "_Odoo_.py"
    open(file_name, 'a').close()
    return file_name


def odoo_test():
    """
    The test class, which includes n tests to assure everything works fine.
    Total tests amount is 2.
    """
    t0 = Field()
    t1 = Field()
    t2 = Field()

    t0.data_name = ("Test", "name")
    t1.data_name = ("Test", "name")
    t2.data_name = ("Python_4ever", "name")
    # Test number 1, class instance t0 is equal to t1
    assert t0.data_name == t1.data_name

    # Test number 2, class instance t1 is NOT equal to t2
    assert t1.data_name != t2.data_name


def main():
    """
    Tha main class which calls all needed functions.
    Functions:
    1. The file function. Call a file function to generate a new python file.
    2. The field collect function. Loops and collect needed field data from the file.
    3. The model collect function. Loops and collect needed field data from the file.
    4. Print out dictionaries keys for a quality purpose.
    5. The write refined data to file function.  Writes file from the refined list of objects.
    6. The end of performace timer.
    """

    # 1. Call a file function to generate a new python file.
    result_file_name = time_stamp_filename()
    # 2. Loops and collect needed field data from the file.
    file_name = "ir_model_fields.xml"
    field_objects = loop_fields(file_name, Field)
    # 3. Loops and collect needed field data from the file.
    file_name = "ir_model.xml"
    model_objects = loop_fields(file_name, Model)
    # 4. Print out dictionaries keys for quality purpose.
    print("MODEL AND FIELD LIST KEYS-->", len(field_objects.keys()))
    print("MODEL OBJECTS LIST KEYS-->", len(model_objects.keys()))
    # 5. Write data function writes an external Python file.
    write_data(field_objects, model_objects, result_file_name)
    # 6. The end of performace timer.
    end = time.time()
    print("Performance result--> ", end - start)


if __name__ == "__main__":
    # A start time for a performance track.
    start = time.time()
    odoo_test()
    main()
