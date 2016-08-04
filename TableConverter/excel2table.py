import xlrd
import os
import copy
import json
from collections import OrderedDict


class Table:

    def __init__(self, sheet, is_root):
        self.name = sheet.name
        self.is_root = is_root
        self.col_names = []
        self.descriptors = []
        self.idx_map = {}

        self.init_col_names(sheet)
        self.init_descriptors(sheet)
        if is_root:
            self.init_idx_map()

    def init_col_names(self, sheet):
        row = sheet.row_values(0)
        for value in row:
            self.col_names.append(value)

    def init_descriptors(self, sheet):
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            self.descriptors.append(self.get_descriptor(row))

    def get_descriptor(self, row):
        descriptor = OrderedDict()
        for i in range(0, len(row)):
            key = self.col_names[i]
            if key[0] == '_':
                continue

            descriptor[key] = row[i]

        return descriptor

    def init_idx_map(self):
        for descriptor in self.descriptors:
            id = descriptor['id']
            self.idx_map[id] = self.descriptors.index(descriptor)

    def merge_child_table(self, child_table):
        if child_table.is_root:
            print(self.name + ' table is root table, merge failed')
            return

        self.add_child_list(child_table)

        for descriptor in child_table.descriptors:
            if('*parent' not in descriptor):
                print(self.name + ' table is not child table')
                continue

            parent_id = descriptor['*parent']
            parent_idx = self.idx_map[parent_id]
            parent_descriptor = self.descriptors[parent_idx]

            child_descriptor = copy.deepcopy(descriptor)
            del child_descriptor['*parent']

            parent_descriptor[child_table.name].append(child_descriptor)

    def add_child_list(self, child_table):
        self.col_names.append(child_table.name)
        for descriptor in self.descriptors:
            descriptor[child_table.name] = []

    def save_to_json(self, pretty_print):
        if not self.is_root:
            print(self.name + ' table is child table, save failed')
            return

        if pretty_print:
            string = json.dumps(self.descriptors, ensure_ascii=False, indent=4)
        else:
            string = json.dumps(self.descriptors, ensure_ascii=False)

        with open(self.name + '.json', 'w') as f:
            f.write(string)


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
        root_table = Table(root_sheet, True)
        print('Convert starting... root table is ' + root_sheet.name)

        for i in range(1, len(sheets)):
            child_sheet = sheets[i]
            if(child_sheet.name[0] == '_'):
                continue

            child_table = Table(child_sheet, False)
            root_table.merge_child_table(child_table)

        root_table.save_to_json(self.pretty_print)
        print('Done')
