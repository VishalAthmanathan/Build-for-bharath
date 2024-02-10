import pandas as pd
import json
import os

allFiles = os.listdir("Datasets")
allColumnNames = {}
mandatoryColumnData = ["product image", "product name", "product description", "maximum retailing price", "selling price", "inventory", "product category", "manufacturer", "product specification", "key features"]
for csvFile in allFiles:
    try:
        if csvFile.split(".")[-1] == "csv":
            data = pd.read_csv("Datasets/" + csvFile)
            allColumnNames[csvFile] = list(data.columns)
            print(csvFile + "\t\u2713 Done")
    except:
        continue
jsondata = json.dumps(allColumnNames, indent=2)
with open("columnsData.json", "w") as outfile:
    outfile.write(jsondata)

