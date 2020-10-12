from testimg import productsImagess
import json, csv

images = productsImagess()

images.pullData()
print(images.read())

images.downloadCSV()

print("\n\n\n")
print(images.getDataById(417))