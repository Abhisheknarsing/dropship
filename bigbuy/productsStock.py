import requests, json, csv
class productsStock:

  def __init__(self):
    print("***************")
    print("Products stock Object Created")
    print("***************\n")

  def pullData(self):
  	endpoint = "https://api.bigbuy.eu/rest/catalog/productsstock.json?isoCode=en"
  	headers = {"Authorization": "Bearer NGFkMzI5NGIwMDM1ZmM2ODNkYTZmYTQ3Nzk3MjNjNDNlN2QwZGE5NWIyMjg1YWRkNDA0NzVkOTc1OTA0NTM1NA"}
  	self.data = requests.get(endpoint, headers=headers).json()
  	return "Products Information pulled"

  def read(self):
  	return self.data

  def getDataById(self,id):
    result=""
    for x in self.data:
      if x['id'] == id:
        result = x['stocks'][0]['quantity']
        break
      else:
        result = "none"
    return result

  def downloadCSV(self):
    products = []
    for emp in self.data:
    	products.append(ProductStock(emp['id'],emp['sku'],emp['stocks'][0]['quantity']))
    with open('productstock.csv', 'w', newline='', encoding="utf-8") as csvfile:
    	spamwriter = csv.writer(csvfile)
    	for record in products:
    		spamwriter.writerow([record.id,record.sku,record.quantity])


class ProductStock:
  def __init__(self, id,sku,quantity):
    self.id = id
    self.sku = sku
    self.quantity = quantity