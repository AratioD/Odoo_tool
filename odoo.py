import xml.etree.ElementTree as ET


# class ValidString:
#     """
#     The class ValidString validates all string based values in the module. 
#     Numerical values are not allowed and string needs to have a prober length, which user defines.
#     """

#     def __init__(self, min_lenght=None):
#         self.min_lenght = min_lenght

#     def __set_name__(self, owner_class, property_name):
#         self.property_name = property_name

#     def __set__(self, instance, value):
#         if not isinstance(value, str):
#             raise ValueError(f'ERROR! {self.property_name} MUST BE A STRING!')
#         if self.min_lenght is not None and len(value) < self.min_lenght:
#             raise ValueError(
#                 f'ERROR! {self.property_name} MUST BE AT LEAST {self.min_lenght} CHARACTERS!'
#             )
#         instance.__dict__[self.property_name] = value

#     def __get__(self, instance, owner_class):
#         if instance is None:
#             return self
#         return instance.__dict__.get(self.property_name, None)


# class Model:
#     ttype = ValidString(2)
#     name = ValidString(2)
#     model = ValidString(2)

class Data:
    def __init__(self):
        self._file = None
        self._sheet_name = None
        self._column_A = None
        self._column_B = None
        self._column_C = None
        self._column_D = None
        self._column_E = None
        self._sheet_index = 0
        self._hash_object = 0
        self._hash_key_object = 0

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        if len(file) < 1:
            raise ValueError("MISSING FILE NAME")
        else:
            self._file = os.path.basename(file)
    #******************
    @property
    def sheet_name(self):
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, sheet_name):
        self._sheet_name = sheet_name
    #******************

    @property
    def column_A(self):
        return self._column_A

    @column_A.setter
    def column_A(self, val):
        # Unpacking column_A and Sheet index
        column_A, sheet_index = val
        self._column_A = str(column_A)

    @property
    def column_B(self):
        return self._column_B


def loop_ir_model_fields(p):

    tree = ET.parse('ir_model_fields.xml')
    root = tree.getroot()
    # # print(root.tag)
    # # print(root[0][1].text)
    for child in root:
        # print(child.tag, child.attrib)
        # print(root[0][0].text)
        for cc in child:
            rank = cc.get('name')
            if rank == "model":
                print("model->", cc.text)
                p.name = cc.text
            elif rank == "name":
                print("name->", cc.text)
                p.name = cc.text
            elif rank == "ttype":
                print("ttype->", cc.text)
                p.name = cc.text


def main():
    """
    Tha main class which calls all needed functions.
    """
    p = Model()
    loop_ir_model_fields(p)


if __name__ == "__main__":
    main()
