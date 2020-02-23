import win32com.client as com_client
import os


excel = com_client.Dispatch("Excel.Application") #создаю ком объект Excel
excel.Visible = False
f = 0
tables = {} #пустой словарь для хранения данных всех таблиц
td_range = input("Please enter data range in format 'A1:D27': ")
td_range.upper()
print()
while True: #открываю таблицы и записываю данные из таблиц в словарь
    file_name = input("""Please enter file name for add in script,
if no more files to add in script type 'end': """)
    print()
    file_path = "C:\\Users\\7700-03-087\\Desktop\\{}.xlsx".format(file_name)
    
    if os.path.isfile(file_path):
        wb = excel.Workbooks.Open(file_path)
        ws = wb.Worksheets("Лист1")
        table = [row for row in ws.Range(td_range).Value if row != (None, None, None, None)]
        tables[f] = tuple(table)
        wb.Close(SaveChanges = False)
        if f == 0:
            svod = file_name
        f += 1
        print()
    elif file_name == "end":
        table = None
        break
    else:
        print("File '{}' do not exist in the dirrectory C:\\Users\\7700-03-087\\Desktop\\".format(file_name))
        print("Chek the correct file name\n")


wb = excel.Workbooks.Open("C:\\Users\\7700-03-087\\Desktop\\{}.xlsx".format(svod)) #открываю свод таблицу
ws = wb.Worksheets("Лист1")
for i in range(1, len(tables)): #записываю отработанные строки в свод
    for row1 in tables[i]:
        x = 0
        if row1[3] != None:
            for row0 in tables[0]:
                x += 1
                if row1[1] in row0 and row0[3] == None:
                    ws.Range("D{}".format(x)).Value = row1[3]
                    ws.Range("C{}".format(x)).Value = row1[2]
wb.Close(SaveChanges = True) #сохраняю изменения


new_name = input("Enter a name for the new workbook: ") #создаю новую таблицу с неотработанными строками
wb = excel.Workbooks.Add()
ws = wb.ActiveSheet
ws.Range(td_range[:-2] + "1").Value = tables[0][0] #записываю заголовок в первую строку
y = 1
for i in range(1, len(tables)): #записываю неотрабатанные строки по порядку из словаря
    for row in tables[i]:
        if row[2] == 2:
            y += 1
            ws.Range("A{}:D{}".format(y, y)).Value = row
wb.SaveAs("C:\\Users\\7700-03-087\\Desktop\\{}.xlsx".format(new_name)) #сохраняю таблицу в директорию по умолчанию
wb.Close(SaveChanges = False)
ws, wb = None, None
excel.Application.Quit()
excel = None
