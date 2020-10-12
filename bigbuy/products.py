import requests, json, csv
class products:

  def __init__(self):
    print("***************")
    print("Products Object Created")
    print("***************\n")

  def pullData(self):
  	endpoint = "https://api.bigbuy.eu/rest/catalog/products.json?isoCode=en"
  	headers = {"Authorization": "Bearer NGFkMzI5NGIwMDM1ZmM2ODNkYTZmYTQ3Nzk3MjNjNDNlN2QwZGE5NWIyMjg1YWRkNDA0NzVkOTc1OTA0NTM1NA"}
  	self.data = requests.get(endpoint, headers=headers).json()
  	return "Products pulled"

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
      products.append(Product(emp['id'],emp['sku'],emp['ean13'],emp['weight'],emp['height'],emp['width'],emp['depth'],emp['dateUpd'],emp['category'],emp['wholesalePrice'],emp['retailPrice'],emp['taxRate'],emp['taxId'],emp['inShopsPrice']))

    with open('products1.csv', 'w', newline='', encoding="utf-8") as csvfile:
      spamwriter = csv.writer(csvfile)
      for record in products:
        spamwriter.writerow([record.id,record.sku,record.ean13,record.weight,record.height,record.width,record.depth,record.category,record.wholesalePrice,record.retailPrice,record.taxRate,record.taxId,record.inShopsPrice])


class Product:
  def __init__(self, id,sku,ean13,weight,height,width,depth,dateUpd,category,wholesalePrice,retailPrice,taxRate,taxId,inShopsPrice):
    self.id = id
    self.sku = sku
    self.ean13 = ean13
    self.weight = weight
    self.height = height
    self.width = width
    self.depth = depth
    self.dateUpd = dateUpd
    self.category = category
    self.wholesalePrice = wholesalePrice
    self.retailPrice = retailPrice
    self.taxRate = taxRate
    self.taxId = taxId
    self.inShopsPrice = inShopsPrice



import requests, json, csv
class productsImages:

  def __init__(self):
    print("***************")
    print("Product Image Object Created")
    print("***************\n")

  def pullData(self):
    endpoint = "https://api.bigbuy.eu/rest/catalog/productsimages.json?isoCode=en"
    headers = {"Authorization": "Bearer NGFkMzI5NGIwMDM1ZmM2ODNkYTZmYTQ3Nzk3MjNjNDNlN2QwZGE5NWIyMjg1YWRkNDA0NzVkOTc1OTA0NTM1NA"}
    self.data = requests.get(endpoint, headers=headers).json()
    return "Products Information pulled"

  def read(self):
    return self.data
    
  def getDataById(self,id):
    result=""
    for x in self.data:
      if x['id'] == id:
        img=""
        count=0
        for y in x['images']:
          if count==0:
            img = y['url']
            count=count+1
          else:
            img = img+";"+y['url']
        result = img
    return result

  def downloadCSV(self):
    products = []
    for emp in self.data:
      img=""
      count=0
      for x in emp['images']:
        if count==0:
          img = x['url']
          count=count+1
        else:
          img = img+";"+x['url']
      products.append(Productimg(emp['id'],img))

    with open('productsImages.csv', 'w', newline='', encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile)
        for record in products:
          spamwriter.writerow([record.id,record.images])

class Productimg:
  def __init__(self, id,images):
    self.id = id
    self.images = images