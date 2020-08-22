"""
2020-08-17 Demo software. @AratioD
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
    Numerical values are not allowed and strings validation rules are.
    1. If "ttype" capitalize a first letter.
    2. If data type is "name" and string starts with "x_". Cut the "x_ value"
    3. If data type is "model". No modifications.
    4. If data type is "field_description". No modifications.
    5. If data type is "class". No modifications.
    Please note that descriptor also saves instances type!
    """

    def __init__(self, min_lenght=None):
        self.min_lenght = min_lenght

    def __set_name__(self, owner_class, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        # Unpack the actual value and value type.
        value, value_type = value
        if not isinstance(value, str):
            raise ValueError(
                f'ERROR! {self.property_name} MUST BE A STRING! NOW IT IS --> {value}')
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
        elif value_type == "model" or value_type == "field_description" or value_type == "class":
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
    A instance attribute can handle only string data type.
    Class instances are Number inside parenthesis define the lenght of the string.
    1. data_type = ValidString(1)
    """
    data_model = ValidString(1)


class Field:
    """
    All instance attributes can handle only string data types.
    Class instances are Number inside parenthesis define the lenght of the string.
    1. data_type = ValidString(1)
    2. data_name = ValidString(1)
    3. data_model = ValidString(1)
    4. data_class = ValidString(1)
    5. data_name_or_inherit = ValidString(1)
    6. data_desc = ValidString(0)
    """
    data_type = ValidString(1)
    data_name = ValidString(1)
    data_model = ValidString(1)
    data_class = ValidString(1)
    data_name_or_inherit = ValidString(1)
    data_desc = ValidString(0)


def loop_fields(file_name, Class):
    """
    Keyword arguments:
    Class -- takes an input Model() or Field() class.
    file_name -- takes input file location.
    Parameters
    The fields are
    1. model
    2. name
    3. ttype
    4. field description
    Returns: A object_set full Model() instances.
    """
    
    object_dict = defaultdict(set)
    # Specified file name.

    full_file = os.path.abspath(os.path.join(file_name))
    dom = ElementTree.parse(full_file)
    # <record model="ir.model.fields" from XML file
    records = dom.findall('record')

    # Checkout how to make this sorter
    for c in records:

        p = Class()
        # print(type(p), id(p), hex(id(p)))
        elem0 = c.find('.//field[@name="model"]')
        # if elem0 is not None:


        if elem0 is not None and elem0.text in object_dict.keys():

            # p.data_model = (elem0.text, "model")
            # Insert first key in the dict
            # object_set.clear()
            object_dict[elem0.text]

            # Loop only if the class is Field()
            if Class is Field:
                object_set = set()
                elem1 = c.find('.//field[@name="name"]')
                if elem1 is not None:
                    p.data_name = (elem1.text, "name")
                    object_set.add(p.data_type)
                    
                elem2 = c.find('.//field[@name="ttype"]')
                if elem2 is not None:
                    p.data_type = (elem2.text, "ttype")
                    object_set.add(p.data_type)

                elem3 = c.find('.//field[@name="field_description"]')
                if elem3 is not None:
                    p.data_desc = (elem3.text, "field_description")
                    object_set.add(p.data_desc)

            object_dict[elem0.text] = object_set
            
        elif elem0 is not None:
            new_set = set()
            
            new_set = object_dict[elem0.text]
            
            # Loop only if the class is Field()
            if Class is Field:
                elem1 = c.find('.//field[@name="name"]')
                if elem1 is not None:
                    p.data_name = (elem1.text, "name")
                    new_set.add(p.data_type)

                elem2 = c.find('.//field[@name="ttype"]')
                if elem2 is not None:
                    p.data_type = (elem2.text, "ttype")
                    new_set.add(p.data_type)

                elem3 = c.find('.//field[@name="field_description"]')
                if elem3 is not None:
                    p.data_desc = (elem3.text, "field_description")
                    new_set.add(p.data_desc)
            
            object_dict[elem0.text] = new_set
            

    return object_dict


def refine_model(elem):
    """
    The function is callable from the function refine_data.
    """
    # An empty initialization of class_name function.
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

    print(len(field_objects.keys()))
    print(len(model_objects.keys()))

    all_models = set()
    # field_models, types = zip(*field_objects)
    # model_models, types = zip(*model_objects)
    # # Unite all models
    # all_models = field_models + model_models

    # # Transform all_models form to set. No duplicates.
    # all_models = set(all_models)

    # Collect all models to one list
    for k in field_objects.keys():
        all_models.add(k)

    for k in model_objects.keys():
        all_models.add(k)

    for models in all_models:
        if models not in field_objects.keys() and models in model_objects.keys():
            print("model no field yes model->", models[0])
            class_name = refine_model(models[0])
            print(class_name)
            # write_rows(model_objects[models[0]], f)
            for ii in model_objects[models[0]]:
                print(ii)

            # row1 = (f'class {elem1.data_class[0]}(models.Model):')
            # f.write('\n')
            # f.write(row1)
            # f.write('\n')
            # row2 = (
            #     f'      {elem1.data_name_or_inherit[0]} = \'{elem1.data_model[0]}\'')
            # f.write(row2)
            # f.write('\n')
            # row3 = (
            #     f'      {elem1.data_name[0]} = fields.{elem1.data_type[0]}(string="{elem1.data_desc[0]}")')
            # f.write(row3)
            # f.write('\n')
            # elif check == True:
            # row3 = (
            #     f'      {elem1.data_name[0]} = fields.{elem1.data_type[0]}(string="{elem1.data_desc[0]}")')
            # f.write(row3)
            # f.write('\n')
        elif models in field_objects.keys() and models not in model_objects.keys():
            print("model yes field not model->", models[0])
            for ii in field_objects[models]:
                print(ii)
        elif models in field_objects.keys() and models in model_objects.keys():
            print("yes field and yes model->", models[0])


def write_rows(dictionary, f):
    print(type(dictionary))
    for ii in dictionary:
        print(ii.data_name)
    # if check == False:
    #     row1 = (f'class {elem1.data_class[0]}(models.Model):')
    #     f.write('\n')
    #     f.write(row1)
    #     f.write('\n')
    #     row2 = (
    #         f'      {elem1.data_name_or_inherit[0]} = \'{elem1.data_model[0]}\'')
    #     f.write(row2)
    #     f.write('\n')
    #     row3 = (
    #         f'      {elem1.data_name[0]} = fields.{elem1.data_type[0]}(string="{elem1.data_desc[0]}")')
    #     f.write(row3)
    #     f.write('\n')
    # elif check == True:
    #     row3 = (
    #         f'      {elem1.data_name[0]} = fields.{elem1.data_type[0]}(string="{elem1.data_desc[0]}")')
    #     f.write(row3)
    #     f.write('\n')


def time_stamp_filename():
    """
    The Function creates a new python file and generates a time stamp for that.
    Return: File name
    """
    timestamp = time.time()
    readable = datetime.datetime.fromtimestamp(timestamp).isoformat()
    timestamp = re.sub("[-:]", "_", readable)
    file_name = str(timestamp) + "_Odoo_.py"
    open(file_name, 'a').close()
    return file_name


# def odoo_test():
#     """
#     The test class, which includes n tests to assure everything works fine.
#     Total tests amount is 5.
#     """
#     t0 = Model()
#     t1 = Model()
#     t2 = Model()
#     t3 = Model()
#     t4 = Model()
#     t5 = Model()
#     t6 = Model()

#     t0.data_name = ("Test", "name")
#     t1.data_name = ("Test", "name")
#     t2.data_name = ("Python_4ever", "name")
#     t3.data_model = ("cat", "model")
#     t4.data_name = ("cat", "name")
#     t5.data_type = ("python_33", "ttype")
#     t6.data_type = ("python_33", "ttype")

#     # Test number 1, class instance t0 is equal to t1
#     assert t0.data_name == t1.data_name

#     # Test number 2, class instance t1 is NOT equal to t2
#     assert t1.data_name != t2.data_name

#     # Test number 3, class instance t3 is NOT equal to t4 for datatype.
#     assert t3.data_model != t4.data_name

#     # Test number 4, class instance t5 is equal to t6 for datatype.
#     assert t5.data_model == t6.data_name

#     # Test number 5, class instance t6 is NOT equal to t0 for datatype.
#     assert t6.data_model != t0.data_name


def main():
    """
    Tha main class which calls all needed functions.
    Functions:
    1. The file function. Call a file function to generate a new python file.
    2. The field collect function. Loops and collect needed field data from the file.
    3. The model collect function. Concanate and refine model data and field data.
    4. The refine data function. Concanate and refine model data and field data
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
    # print("MODEL AND FIELD LIST SIZE-->", len(model_and_fields))
    # print("MODEL OBJECTS LIST SIZE-->", len(model_objects))
    # for k, v in model_objects.keys():
    #     print(k)

    for k, v in field_objects.items():
        # print("key-->", k, "value-->", v)
        for vv in v:
            print(v)

    # for k, v in model_objects.items():
    #     print("key-->", k, "value-->", v)

    # for i in model_objects:
    #     print(type(i), "--", id(i), i.__dict__)
    #     print(isinstance(i, Field))
    # print(id(i))
    # inherit_models, name_models, empty_models = individual_models(
    #     model_and_fields, model_objects)

    # # 4. Concanate and refine model data and field data
    # refined_objects = refine_data(
    #     model_and_fields, inherit_models, name_models, empty_models)

    # # 5. Writes file from the refined list of objects.
    # write_data(field_objects, model_objects, result_file_name)
    #            inherit_models, name_models, empty_models)

    # 6. The end of performace timer.
    end = time.time()
    print("Performance result--> ", end - start)


if __name__ == "__main__":
    """
    Two functions
    """
    # A start time for a performance comparision.
    start = time.time()
    # Run unit tests.
    # odoo_test()
    main()
