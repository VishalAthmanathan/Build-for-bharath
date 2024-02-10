from termcolor import colored, cprint
import json
import re
import pandas as pd
class Catalogue:

    def __init__(self):
        pass

    def open(self, filename):
        fileExtension = filename.split(".")[-1]
        if fileExtension == "csv":
            self.CatalogueData = pd.read_csv(filename)
            return self.CatalogueData
        
        elif fileExtension == ".json":
            pass
        
        elif fileExtension == "xlsx":
            pass

    def information(self):
        try:
            columnsList = list(self.CatalogueData.columns)
            dtypesList = [str(i) for i in self.CatalogueData.dtypes]
            self.catalogueInformation = {}
            for i in range(len(columnsList)):
                self.catalogueInformation[columnsList[i].lower()] = dtypesList[i]
            return self.catalogueInformation
        except AttributeError:
            pass


class AttributesScoring:
    def __init__(self, filename):
        self.catalogue = Catalogue()
        self.catalogueData = self.catalogue.open(filename)
        self.catalogueAttributes = {}
        self.AttributesFile = "columns.json"
        self.attributesDictionary = {}

    def check(self):
        self.catalogueInformation = self.catalogue.information()
        self.attributeList = []
        self.readAttributes()
        for attribute in self.catalogueInformation:
            cleanAttribute = re.sub(r'[^a-zA-Z0-9]', '', attribute).lower()
            self.attributeList.append(cleanAttribute)
            self.identifyAttribute(cleanAttribute)

    def readAttributes(self):
        with open(self.AttributesFile, 'r') as file:
            self.Attributes = json.load(file)
        for attributes in self.Attributes["columns"]:
            self.attributesDictionary[attributes] = [0]
    
    def identifyAttribute(self, attribute):
        for attributes in self.Attributes["columns"]:
            for token in self.Attributes["columns"][attributes][0]:
                if token == attribute or attribute in token: 
                    self.attributesDictionary[attributes][0] = 1
                    self.attributesDictionary[attributes].append(attribute)
                    return True
        return False

    def score(self):
        total = 0
        score = 0
        self.check()
        for attribute in self.attributesDictionary:
            total += 1
            if self.attributesDictionary[attribute][0] == 1:
                score += 1
        print("")
        cprint(f"-> Score: {score}/{total}", "black", "on_light_cyan")
        print("\n----------------")
        cprint("Recommendations:", "light_yellow")
        print("----------------")
        self.recommendation()

    def recommendation(self):
        columnNamedProperly = []
        for attribute in self.attributesDictionary:
            if self.attributesDictionary[attribute][0] == 0:
                print(colored(f"Add: {attribute.capitalize()}", color="light_green"))
            elif self.attributesDictionary[attribute][0] == 1:
                columnNamedProperly.append(self.attributesDictionary[attribute][1])

        for attribute in self.attributeList:
            if attribute not in columnNamedProperly:
                print(colored(f"Rename: {attribute} [optional]", color="light_red"))
            elif "unname" in attribute.lower():
                print(colored(f"Remove: {attribute}", color="light_red"))

if __name__ == "__main__":
    catalogue = Catalogue()
    filename = input("Enter Filename: ")
    catalogue.open(filename)
    print(catalogue.information())
    CatalogueCheck1 = AttributesScoring(filename=filename)
    CatalogueCheck1.score()