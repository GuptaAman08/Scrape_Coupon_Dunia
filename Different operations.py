import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from time import sleep
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)





def create_spreadsheet(name):
    sh = client.create(name)
    return sh

def share_with_other_email(sh, email, p_type, user_role):
    sh.share(email, perm_type=p_type, role=user_role)

def open_by_title(title):
    sh = client.open(title)
    return sh

def open_by_url(url):
    sh = client.open_by_url(url)
    return sh

def create_worksheet(name, row, col):
    worksheet = sh.add_worksheet(title=name, rows=row, cols=col)
    return worksheet

def select_worksheet_by_index(index):
    worksheet = sh.get_worksheet(index)
    return worksheet

def select_worksheet_by_title(title):
    worksheet = sh.worksheet(title)
    return worksheet

def get_all_worksheets():
    worksheet_list = sh.worksheets()
    return worksheet_list

def delete_worksheet(inst):
    # pass woksheet explicitly
    sh.del_worksheet(inst)

def get_a_cell_value(cell):
    # like cell as 'A1'
    val = worksheet.acell(cell).value
    return val

def get_a_row_value(num):
    values_list = worksheet.row_values(num)
    return values_list

def get_a_col_value(num):
    values_list = worksheet.col_values(num)
    return values_list

def insert_row(sh, row):
    sh.append_row(values=row)

def update_a_cell(worksheet, cell, val):
    # val => value to update, cell => like "A!" 
    worksheet.update_acell(cell, val)

def list_all_data(ws):
    # Extract and print all of the values
    list_of_lists = ws.get_all_values()
    pprint(list_of_lists)


if __name__ == "__main__":
    # sh = create_spreadsheet("practice")
    # sleep(2)
    # share_with_other_email(sh, "aman.gupta@tacto.in", "user", "writer")
    # sleep(5)
    sh = open_by_title("practice")
    sh = sh.sheet1

    update_a_cell(sh, 'A1', "Updated this cell through code.")
    # insert_row(sh, ["First", "Second", "Third"])




