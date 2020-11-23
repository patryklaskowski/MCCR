import openpyxl

class Excel(object):

    count = 0
    XLSX_DEFAULT_COLUMNS = list('abcdefghijklmnopqrstuvwxyz'.upper())

    def __init__(self):
        Excel.count += 1
        # print(f'There is {Excel.count} Excel class objects currently...')

    def __assert_file_exist__(self):
        assert self.file, "No excel file found..."

    def create_empty_workbook(self, path):
        file = openpyxl.Workbook()
        file.save(path)

    def from_path(self, path):
        self.path = path
        self.file = openpyxl.load_workbook(path)
        self.sheet = self.file.active
        self.__assert_file_exist__()

    def create_column_names(self, columns_names):
        self.__assert_file_exist__()
        assert len(columns_names) <= len(Excel.XLSX_DEFAULT_COLUMNS), f'Too many columns names provided (max {len(XLSX_DEFAULT_COLUMNS)})'
        for idx, name in enumerate(columns_names):
            self.sheet[f'{Excel.XLSX_DEFAULT_COLUMNS[idx]}1'] = name

    def append_row(self, row):
        self.__assert_file_exist__()
        self.sheet.append(row)

    def save(self):
        self.__assert_file_exist__()
        self. file.save(self.path)
