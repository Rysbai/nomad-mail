import xlrd


COLS = {
    'distance': 3,
    'surname': 4,
    'name': 5,
    'birth_date': 7,
    'sex': 8,
    'country': 11,
    'phone': 18,
    'email': 20,
    'register_date': 36,
    'pay_status': 37
}


def parse_xls(file_name):
    data = []
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)

    for row in range(2, sheet.nrows):
        recipient_data = {}
        for key, col_num in COLS.items():
            value = sheet.cell_value(row, col_num - 1)
            recipient_data[key] = value if value else ''

        data.append(recipient_data)
    return data
