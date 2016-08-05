import xlrd
import os
import copy
import json
from collections import OrderedDict


class Table:

    def __init__(self, sheet):
        self.init_name(sheet)
        self.init_parent_name(sheet)
        self.init_metadata(sheet)
        self.init_descriptors(sheet)
        self.init_id_index_map()

    def init_name(self, sheet):
        self.name = sheet.name

    def init_parent_name(self, sheet):
        row = sheet.row_values(0)
        self.parent_name = row[0]
        if type(self.parent_name) is not str:
            raise Exception('Parent name is not string')

        self.is_root = self.parent_name == '*root'

    def init_metadata(self, sheet):
        row = sheet.row_values(1)
        self.is_parent = False
        self.is_child = False
        self.column_names = []
        for value in row:
            if type(value) is not str:
                raise Exception('Column name is not string')

            if value == 'id':
                self.is_parent = True
            if value == '*parent':
                self.is_child = True
            self.column_names.append(value)

        if self.is_root and self.is_child:
            raise Exception('Root table must not have "*parent" column')

        if not self.is_root and not self.is_child:
            raise Exception('Child table must have "*parent" column')

    def init_descriptors(self, sheet):
        self.descriptors = []
        for i in range(2, sheet.nrows):
            row = sheet.row_values(i)
            self.descriptors.append(self.get_descriptor(row))

    def init_id_index_map(self):
        if not self.is_parent:
            return

        self.id_index_map = {}
        for descriptor in self.descriptors:
            id = descriptor['id']
            self.id_index_map[id] = self.descriptors.index(descriptor)

    def get_descriptor(self, row):
        descriptor = OrderedDict()
        for i in range(0, len(row)):
            key = self.column_names[i]
            if key[0] == '_':
                continue

            descriptor[key] = row[i]

        return descriptor

    def merge_child_table(self, table):
        self.add_child_descriptor_list(table.name)
        for descriptor in table.descriptors:
            parent_id = descriptor['*parent']
            parent_idx = self.id_index_map[parent_id]
            parent_descriptor = self.descriptors[parent_idx]
            parent_descriptor[table.name].append(descriptor)

    def add_child_descriptor_list(self, name):
        for descriptor in self.descriptors:
            descriptor[name] = []

    def remove_parent_column(self):
        for descriptor in self.descriptors:
            del descriptor['*parent']

    def save_to_json(self, pretty_print):
        if pretty_print:
            string = json.dumps(self.descriptors, ensure_ascii=False, indent=4)
        else:
            string = json.dumps(self.descriptors, ensure_ascii=False)

        with open(self.name + '.json', 'w') as f:
            f.write(string)


class Converter:

    def __init__(self, pretty_print):
        self.pretty_print = pretty_print

    def convert(self, filename):
        print(filename + 'convert starting...')

        sheets = Converter.get_sheets(filename)

        root_table, tables = Converter.get_tables(sheets)

        Converter.post_process(tables)

        root_table.save_to_json(self.pretty_print)

        print('Done')

    def get_sheets(filename):
        path = os.path.abspath(filename)
        workbook = xlrd.open_workbook(path)
        return workbook.sheets()

    def get_tables(sheets):
        tables = {}
        root_tables = []

        for sheet in sheets:
            if sheet.name[0] == '_':
                continue

            table = Table(sheet)
            tables[table.name] = table
            if table.is_root:
                root_tables.append(table)

        if len(root_tables) == 1:
            return root_tables[0], tables
        else:
            raise Exception('Root table must be one')

    def post_process(tables):
        for name, table in tables.items():
            if table.is_root:
                continue

            parent_table = tables[table.parent_name]
            if not parent_table.is_parent:
                raise Exception('Parent table must have id column')

            parent_table.merge_child_table(table)
            table.remove_parent_column()
