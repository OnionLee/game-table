import xlrd
import os
import copy
import json
from collections import OrderedDict


class Table:

    def __init__(self, sheet):
        self.col_names = []
        self.descriptors = []
        self.name = sheet.name

        self.get_col_names(sheet)
        self.get_descriptors(sheet)

    def get_col_names(self, sheet):
        row = sheet.row_values(0)
        for value in row:
            self.col_names.append(value)

    def get_descriptors(self, sheet):
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            self.descriptors.append(self.get_descriptor(row))

    def get_descriptor(self, row):
        descriptor = OrderedDict()
        for j in range(0, len(row)):
            key = self.col_names[j]
            if key[0] == '_':
                continue

            descriptor[key] = row[j]

        return descriptor

    def get_descriptors_by_id(self, id):
        descriptors = []
        for descriptor in self.descriptors:
            if '*parent' not in descriptor:
                print(descriptor)
                print(self.name + ' : this table is root table')
                return descriptors
            elif descriptor['*parent'] == id:
                #*parent를 지우기 위해 카피본을 만듦
                clone = copy.deepcopy(descriptor)
                del clone['*parent']
                descriptors.append(clone)

        return descriptors

    def merge(self, table):
        self.col_names.append(table.name)
        for descriptor in self.descriptors:
            id = descriptor['id']
            descriptor[table.name] = table.get_descriptors_by_id(id)

    def to_json(self, pretty):
        if pretty:
            return json.dumps(self.descriptors, ensure_ascii=False, indent=4)
        else:
            return json.dumps(self.descriptors, ensure_ascii=False)


class Converter:

    def __init__(self, pretty_print):
        self.pretty_print = pretty_print

    def get_workbook(filename):
        path = os.path.abspath(filename)
        return xlrd.open_workbook(path)

    def convert(self, filename):
        workbook = Converter.get_workbook(filename)
        sheets = workbook.sheets()

        root_sheet = sheets[0]
        root_table = Table(root_sheet)
        print('Convert starting... root table is ' + root_sheet.name)

        for i in range(1, len(sheets)):
            child_sheet = sheets[i]
            if(child_sheet.name[0] == '_'):
                continue

            child_table = Table(child_sheet)
            root_table.merge(child_table)

        json = root_table.to_json(self.pretty_print)
        with open(root_table.name + '.json', 'w') as f:
            f.write(json)

        print('Done')
