"""
2020-08-07 Demo software. @AratioD
"""
import time
import os
import datetime
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
    All instance attributes can handle only string data types.
    Class instances are Number inside parenthesis define the lenght of the string.
    1. data_type = ValidString(2)
    2. data_name = ValidString(2)
    3. data_model = ValidString(2)
    4. data_name_or_inherit = ValidString(2)
    """
    data_type = ValidString(2)
    data_name = ValidString(2)
    data_model = ValidString(2)
    data_name_or_inherit = ValidString(2)
    data_desc = ValidString(0)


def loop_ir_model_fields(file_name):
    """
    Loop all specified ir model fields.
    The fields are
    1. model
    2. name
    3. ttype
    4. field description
    Returns: A object_list full Model() instances.
    """
    object_list = []
    # Specified file name.

    full_file = os.path.abspath(os.path.join(file_name))
    dom = ElementTree.parse(full_file)
    # <record model="ir.model.fields" from XML file
    records = dom.findall('record')

    for c in records:
        p = Model()

        elem0 = c.find('.//field[@name="model"]')
        if elem0 != None:
            p.data_model = (elem0.text, "model")
        else:
            pass

        elem1 = c.find('.//field[@name="name"]')
        if elem1 != None:
            p.data_name = (elem1.text, "name")
        else:
            pass

        elem2 = c.find('.//field[@name="ttype"]')
        if elem2 != None:
            p.data_type = (elem2.text, "ttype")
        else:
            pass

        elem3 = c.find('.//field[@name="field_description"]')
        if elem3 != None:
            p.data_desc = (elem3.text, "field_description")
        else:
            pass

        object_list.append(p)

    return object_list


def individual_models(model_and_fields, model_objects):
    """
    The function individual_models only task is to encapsulate all unique models
    to one trustful list, where it can looper through in further occasions.
    It takes in
    1. model_and_fields
    2. model_objects
    Returns
    1. _name --> name_models models
    2. _inherit --> inherit models
    3. empty models
    """

    name_models = set()
    inherit_models = set()
    empty_models = set()
    all_models = set()
    temp0_models = set()
    temp1_models = set()

    for m in model_and_fields:
        all_models.add(m.data_model)
        temp0_models.add(m.data_model)

    for m in model_objects:
        all_models.add(m.data_model)
        temp1_models.add(m.data_model)
    # Create a set of _inherit models.
    inherit_models = temp0_models - temp1_models
    # Create a set of _name models.
    name_models = temp0_models.intersection(temp1_models)
    # Create a set of empty_models.
    empty_models = all_models.difference(name_models | inherit_models)

    print(temp0_models, "models and fields")
    print(temp1_models, "model objects")
    print(inherit_models, "lenght of inherit_models", len(inherit_models))
    print(name_models, "lenght of name_models", len(name_models))
    print(empty_models, "emptyModels", len(empty_models))

    return all_models, inherit_models, name_models, empty_models


def refine_data(model_and_fields, inherit_models, name_models, empty_models):
    """
    The function takes two parameters in and returns refined list.
    Parameters are.
    1. model_and_fields
    2. model_objects
    Returns: A object_list full Model() instances.
    """
    # List for refined objects
    refined_objects = set()

    for elem in empty_models:
        ro = Model()
        print(elem)
        ro.data_model = (elem[0], elem[1])
        refined_objects.add(ro)

    for elem in inherit_models:
        for elem1 in model_and_fields:
            if elem[0] == elem1.data_model[0]:
                ro = Model()
                ro.data_model = (elem1.data_model[0], elem1.data_model[1])
                ro.data_name = (elem1.data_name[0], elem1.data_name[1])
                ro.data_type = (elem1.data_type[0], elem1.data_type[1])
                ro.data_desc = (elem1.data_desc[0], elem1.data_desc[1])
                ro.data_name_or_inherit = ("_inherit", "name")
                refined_objects.add(ro)
            else:
                pass

    for elem in name_models:
        for elem1 in model_and_fields:
            if elem[0] == elem1.data_model[0]:
                ro = Model()
                ro.data_model = (elem1.data_model[0], elem1.data_model[1])
                ro.data_name = (elem1.data_name[0], elem1.data_name[1])
                ro.data_type = (elem1.data_type[0], elem1.data_type[1])
                ro.data_desc = (elem1.data_desc[0], elem1.data_desc[1])
                ro.data_name_or_inherit = ("_name", "name")
            else:
                pass

    return refined_objects


def write_data(refined_objects, result_file_name, all_models):
    """
    Writes refined objects to time stamped file name
    Returns: Time-stamped Python file.
    """

    f = open(result_file_name, "a")

    # Imports to py file.
    row0 = (f'from odoo import models, fields')

    f.write(row0)
    f.write('\n')
    f.write('\n')

    for model in all_models:
        #Indicator is False or True
        check = False

        if "." in model[0]:
            class_name = model[0].split(".")
            print(class_name)
            class_name = class_name[1].capitalize()
            # print(".->", class_name)
        elif "_" in model[0]:
            class_name = model[0].split("_")
            class_name = class_name[0] + class_name[1]
            class_name = class_name.capitalize()

        else:
            class_name = model[0]
            class_name = class_name[1].capitalize()

        row1 = (f'class {class_name}(models.Model):')
        f.write('\n')
        f.write(row1)

        for ro in refined_objects:

            if model[0] == ro.data_model[0] and check == False:
                if ro.data_name_or_inherit != None and ro.data_model != None:
                    row2 = (
                        f'      {ro.data_name_or_inherit[0]} = \'{ro.data_model[0]}\'')
                    f.write('\n')
                    f.write(row2)
                    f.write('\n')
                    check = True
            elif model[0] == ro.data_model[0] and check == True:
                if ro.data_name != None and ro.data_type != None and ro.data_desc != None:
                    f.write('\n')
                    row3 = (
                        f'       {ro.data_name[0]} = fields.{ro.data_type[0]}(string="{ro.data_desc[0]}")')
                    f.write('\n')
                    f.write(row3)
                    f.write('\n')



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


def odoo_test():
    """
    The test class, which includes n tests to assure everything works fine.
    Total tests amount is 5.
    """
    t0 = Model()
    t1 = Model()
    t2 = Model()
    t3 = Model()
    t4 = Model()
    t5 = Model()
    t6 = Model()

    t0.data_name = ("Test", "name")
    t1.data_name = ("Test", "name")
    t2.data_name = ("Python_4ever", "name")
    t3.data_model = ("cat", "model")
    t4.data_name = ("cat", "name")
    t5.data_type = ("python_33", "ttype")
    t6.data_type = ("python_33", "ttype")

    # Test number 1, class instance t0 is equal to t1
    assert t0.data_name == t1.data_name

    # Test number 2, class instance t1 is NOT equal to t2
    assert t1.data_name != t2.data_name

    # Test number 3, class instance t3 is NOT equal to t4 for datatype.
    assert t3.data_model != t4.data_name

    # Test number 4, class instance t5 is equal to t6 for datatype.
    assert t5.data_model == t6.data_name

    # Test number 5, class instance t6 is NOT equal to t0 for datatype.
    assert t6.data_model != t0.data_name


def main():
    """
    Tha main class which calls all needed functions.
    Functions:
    1. The file function. Call a file function to generate a new python file.
    2. The field collect function. Loops and collect needed field data from the file.
    3. The model collect function. Concanate and refine model data and field data.
    4. The refine data function. Concanate and refine model data and field data
    5. The write refined data to file function.  Writes file from the refined list of objects.
    5. The end of performace timer.
    """

    # 1. Call a file function to generate a new python file.
    result_file_name = time_stamp_filename()
    # 2. Loops and collect needed field data from the file.
    file_name = "ir_model_fields.xml"
    model_and_fields = loop_ir_model_fields(file_name)
    # 3. Loops and collect needed field data from the file.
    file_name = "ir_model.xml"
    model_objects = loop_ir_model_fields(file_name)
    print("model and field", len(model_and_fields))
    print("lenght model object", len(model_objects))

    all_models, inherit_models, name_models, empty_models = individual_models(
        model_and_fields, model_objects)

    # for i in model_and_fields:
    #     print("model_and_fields-->", i.data_model[0])

    # for i in model_objects:
    #     print("model_objects-->", i.data_model[0])
    # model_objects = loop_ir_model()
    # 4. Concanate and refine model data and field data
    refined_objects = refine_data(
        model_and_fields, inherit_models, name_models, empty_models)

    print("refined objects", len(refined_objects))
    # print("individual models", len(all_models))
    for ii in refined_objects:
        print("****************")
        if ii.data_model != None:
            print(ii.data_model[0])
        else:
            pass
        if ii.data_name != None:
            print(ii.data_name[0])
        else:
            pass
        if ii.data_type != None:
            print(ii.data_type[0])
        else:
            pass
        if ii.data_name_or_inherit != None:
            print(ii.data_name_or_inherit[0])
        else:
            pass
        if ii.data_desc != None:
            print(ii.data_desc[0])
        else:
            pass
        print("****************")

        # elem2 = c.find('.//field[@name="ttype"]')
        # if elem2 != None:
        #     p.data_type = (elem2.text, "ttype")
        # else:
        #     pass

        # elem3 = c.find('.//field[@name="field_description"]')
        # if elem3 != None:
        #     p.data_desc = (elem3.text, "field_description")
        # else:
        #     pass
        #     print(ii.data_model[0], " ", ii.data_name[0], " ",
        #           ii.data_name_or_inherit[0], " ", ii.data_desc[0], " ", ii.data_type[0])

    # for tt in all_models:
    #     print("models", tt[0])

    # 5. Writes file from the refined list of objects.
    write_data(refined_objects, result_file_name, all_models)
    # # A end time for a performance comparision
    print("refined objects", len(refined_objects))
    end = time.time()
    print("Performance result--> ", end - start)


if __name__ == "__main__":
    """
    Two functions
    """
    # A start time for a performance comparision.
    start = time.time()
    # Run unit tests.
    odoo_test()
    main()
