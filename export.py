import csv
import json

def exportToCsv(products):
    keys = ["Title", "Price", "Price Without Discount", "Main Image", "Images", "Rating Score", "Review Count"]

    with open("products.csv", "w", encoding="utf-8", newline='') as fout:
        dict_writer = csv.DictWriter(fout, fieldnames=keys)
        dict_writer.writeheader()
        for product in products: 
            if (not isinstance(product, Exception)):
                dict_writer.writerow(product)


def exportToJson(products):
    with open("products.json", "w") as fout:
            json.dump(products, fout, skipkeys=False)