import win32com.client as com_client
import os

excel = com_client.Dispatch("Excel.Application")
excel.Visible = False


file1 = "C:\\Users\\7700-03-087\\Desktop\\ad.xlsx"
if os.path.isfile(file1):
        wb = excel.Workbooks.Open(file1)
        ws = wb.Worksheets("Лист1")
        ad = [row[0].replace('"', '').split(',')[0:2] for row in ws.Range('A1:A201').Value]
        addict = {x[1]: x[0] for x in ad}
        wb.Close(SaveChanges = False)

file2 = "C:\\Users\\7700-03-087\\Desktop\\stat.xlsx"
if os.path.isfile(file2):
        wb = excel.Workbooks.Open(file2)
        ws = wb.Worksheets("Документ (1)")
        state = [list(row[:2]) for row in ws.Range('A1:C427').Value if "Основной" in row]
        wb.Close(SaveChanges = False)

not_in_ad = list()
job_not_eq_state = list()
for row in state:
        if row[1] not in addict:
                not_in_ad.append(row)
        else:
                if addict[row[1]] != row[0]:
                        print("state: ", row, "\nad: ", addict[row[1]], "\n")
                        job_not_eq_state.append(row)
