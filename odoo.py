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
    object_list = set()
    # Specified file name.

    full_file = os.path.abspath(os.path.join(file_name))
    dom = ElementTree.parse(full_file)
    # <record model="ir.model.fields" from XML file
    records = dom.findall('record')

    print(records)
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
    
        object_list.add(p)

    return object_list


def refine_data(model_and_fields, model_objects):
    """
    The function takes two parameters in and returns refined list.
    Parameters are.
    1. model_and_fields
    2. model_objects
    Returns: A object_list full Model() instances.
    """
    # List for refined objects
    refined_objects = set()
    individual_models = set()
    # objects_dict = defaultdict(set)

    for elem in model_and_fields:
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

        # Collect all possibly datamodels
        individual_models.add(elem.data_model[0])

        ro.data_model = (elem.data_model[0], elem.data_model[1])
        ro.data_name = (elem.data_name[0], elem.data_name[1])
        ro.data_type = (elem.data_type[0], elem.data_type[1])
        ro.data_desc = (elem.data_desc[0], elem.data_desc[1])
        refined_objects.add(ro)
        # objects_dict[elem.data_model[0]] = ro
    return refined_objects, individual_models


def write_data(refined_objects, result_file_name, individual_models):
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

    for model in individual_models:
        # print(model)
        check = False
        # f.write('\n')
        for ro in refined_objects:
            if model == ro.data_model[0] and check == False:
                if "." in ro.data_model[0]:
                    class_name = ro.data_model[0].split(".")
                    class_name = class_name[1].capitalize()
                    print(".->", class_name)
                elif "_" in ro.data_model[0]:
                    class_name = ro.data_model[0].split("_")
                    class_name = class_name[0] + class_name[1]
                    class_name = class_name.capitalize()
                    print("_->", class_name)
                else:
                    class_name = ro.data_model[0].capitalize()
                check = True
                row1 = (f'class {class_name}(models.Model):')
                row2 = (
                    f'      {ro.data_name_or_inherit[0]} = \'{ro.data_model[0]}\'')
                f.write('\n')
                f.write(row1)
                f.write('\n')
                f.write(row2)
                f.write('\n')

            if check == True:
                # f.write('\n')
                row3 = (
                    f'      {ro.data_name[0]} = fields.{ro.data_type[0]}(string="{ro.data_desc[0]}")')
                # f.write('\n')
                f.write(row3)
                f.write('\n')

    # for ro in refined_objects:
    #     # String modifications to class name
    #     if "." in ro.data_model[0]:
    #         class_name = ro.data_model[0].split(".")
    #         class_name = class_name[1].capitalize()
    #         print(".->", class_name)
    #     elif "_" in ro.data_model[0]:
    #         class_name = ro.data_model[0].split("_")
    #         class_name = class_name[0] + class_name[1]
    #         class_name = class_name.capitalize()
    #         print("_->", class_name)
    #     else:
    #         class_name = ro.data_model[0].capitalize()

    #     row1 = (f'class {class_name}(models.Model):')
    #     row2 = (
    #         f'      {ro.data_name_or_inherit[0]} = \'{ro.data_model[0]}\'')
    #     row3 = (f'      {ro.data_name[0]} = fields.{ro.data_type[0]}()')

    #     f.write(row1)
    #     f.write('\n')
    #     f.write(row2)
    #     f.write('\n')
    #     f.write(row3)
    #     f.write('\n')
    #     f.write('\n')


def loop_ir_model(file_name):
    """
    Loop all specified model fields.
    The field is
    1. model
    Returns: A object_list full Model() instances.
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

    for i in model_and_fields:
        print("jee", i.data_model[0])
        
    for i in model_objects:
        print("jee--->", i.data_model[0])
    # model_objects = loop_ir_model()
    # # 4. Concanate and refine model data and field data
    # refined_objects, individual_models = refine_data(
    #     model_and_fields, model_objects)

    # # 5. Writes file from the refined list of objects.
    # write_data(refined_objects, result_file_name, individual_models)
    # # A end time for a performance comparision
    # end = time.time()
    # print("Performance result--> ", end - start)


if __name__ == "__main__":
    """
    Two functions
    """
    # A start time for a performance comparision.
    # start = time.time()
    # Run unit tests.
    # odoo_test()
    main()
