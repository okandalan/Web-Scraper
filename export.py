import csv
import os
from xlsxwriter import Workbook


path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "exported_files")

def exportToCsv(products):
    if (not os.path.exists(path)):
        os.makedirs(path)
    headers = ["Title", "Price", "Price Without Discount", "Main Image",
               "Images", "Rating Score", "Review Count"]

    with open("exported_files/products.csv", "w", encoding="utf-8", newline='') as fout:
        dictWriter = csv.DictWriter(fout, fieldnames=headers)
        dictWriter.writeheader()

        for product in products:
            # Exception objects in products list are skipped 
            if (isinstance(product, dict)):
                dictWriter.writerow(product)

def exportToExcel(products):
    if (not os.path.exists(path)):
        os.makedirs(path)
    headers = ["Title", "Price", "Price Without Discount", "Main Image",
               "Images", "Rating Score", "Review Count"]

    wb = Workbook("exported_files/products.xlsx")
    ws = wb.add_worksheet()

    firstRow = 0
    for i in range(len(headers)):
        col = i
        ws.write(firstRow, col, headers[i])

    row = 1
    for product in products:
        # Exception objects in products list are skipped 
        if (isinstance(product, dict)):
            for _key, _value in product.items():
                col = headers.index(_key)
                # Convert list of image urls to string to write into one excel cell
                if (type(_value) == list):
                    ws.write(row, col, str(_value))
                else:                   
                    ws.write(row, col, _value)
            row += 1
    
    wb.close() 