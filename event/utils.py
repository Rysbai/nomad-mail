import xlrd

from event.constants import CODES


def parse_xls(file_name, cols):
    data = []
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)

    for row in range(2, sheet.nrows):
        recipient_data = {}
        for key, col_num in cols.items():
            value = sheet.cell_value(row, col_num - 1)
            recipient_data[key] = value if value else ''

        data.append(recipient_data)
    return data


def get_col_number(chars):
    if len(chars) == 1:
        return CODES[chars]
    elif len(chars) == 2:
        return CODES[chars[0]] * len(CODES) + CODES[chars[1]]
    else:
        pass

