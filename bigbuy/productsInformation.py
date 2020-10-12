import requests, json, csv
class productsInformation:

  def __init__(self):
    print("***************")
    print("Products Information Object Created")
    print("***************\n")

  def pullData(self):
  	endpoint = "https://api.bigbuy.eu/rest/catalog/productsinformation.json?isoCode=en"
  	headers = {"Authorization": "Bearer NGFkMzI5NGIwMDM1ZmM2ODNkYTZmYTQ3Nzk3MjNjNDNlN2QwZGE5NWIyMjg1YWRkNDA0NzVkOTc1OTA0NTM1NA"}
  	self.data = requests.get(endpoint, headers=headers).json()
  	return "Products Information pulled"

  def read(self):
  	return self.data

  def getDataById(self,id):
    result=""
    for x in self.data:
      if x['id'] == id:
        result = x
        break
      else:
        result = "none"
    return result

  def downloadCSV(self):
  	products = []
  	for emp in self.data:
  		products.append(Productinf(emp['id'],emp['sku'],emp['dateUpdDescription'],emp['isoCode'],emp['url'],emp['description']))
  	with open('products.csv', 'w', newline='', encoding="utf-8") as csvfile:
  		spamwriter = csv.writer(csvfile)
  		for record in products:
  			spamwriter.writerow([record.id,record.sku,record.dateUpdDescription,record.isoCode,record.url,record.description])


class Productinf:
  def __init__(self, id,sku,dateUpdDescription,isoCode,url,description):
    self.id = id
    self.sku = sku
    self.dateUpdDescription = dateUpdDescription
    self.isoCode = isoCode
    self.url = url
    self.description = description


