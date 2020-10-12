import requests, json, csv


class Bigbuy:

  def __init__(self):
    self.productsImagesData = None
    self.productsData = None
    self.productsInformationData = None
    self.productsStockData = None
    self.finalProductsData = None


  def getAuthHeader(self):
    return {"Authorization": "Bearer NGFkMzI5NGIwMDM1ZmM2ODNkYTZmYTQ3Nzk3MjNjNDNlN2QwZGE5NWIyMjg1YWRkNDA0NzVkOTc1OTA0NTM1NA"}

  def pullAllData(self):
    self.productsImagesData = productsImages()
    self.productsData = products()
    self.productsInformationData = productsInformation()
    self.productsStockData = productsStock()
    print("Pullling Images Data...")
    self.productsImagesData.pullData()
    print("Completed\n")
    print("Pulling products Data ...")
    self.productsData.pullData()
    print("Completed \n")
    print("Pulling Products additional information data...")
    self.productsInformationData.pullData()
    print("Completed\n")
    print("Pulling Stock data...")
    self.productsStockData.pullData()
    print("Completed\n")





class products:

  def __init__(self):
    self.bigbuy_credits = Bigbuy()
    pass

  def pullData(self):
    endpoint = "https://api.bigbuy.eu/rest/catalog/products.json?isoCode=en"
    self.data = requests.get(endpoint, headers= self.bigbuy_credits.getAuthHeader() ).json()
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


class productsImages:

  def __init__(self):
    self.bigbuy_credits = Bigbuy()
    pass

  def pullData(self):
    endpoint = "https://api.bigbuy.eu/rest/catalog/productsimages.json?isoCode=en"
    self.data = requests.get(endpoint, headers= self.bigbuy_credits.getAuthHeader() ).json()
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


class productsInformation:

  def __init__(self):
    self.bigbuy_credits = Bigbuy()
    pass

  def pullData(self):
    endpoint = "https://api.bigbuy.eu/rest/catalog/productsinformation.json?isoCode=en"
    self.data = requests.get(endpoint, headers=self.bigbuy_credits.getAuthHeader()).json()
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



class productsStock:

  def __init__(self):
    self.bigbuy_credits = Bigbuy()
    pass

  def pullData(self):
    endpoint = "https://api.bigbuy.eu/rest/catalog/productsstock.json?isoCode=en"
    self.data = requests.get(endpoint, headers=self.bigbuy_credits.getAuthHeader()).json()
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


class finalProducts:
  def __init__(self,id,name,sku,url,ean13,description,tags,wholesalePrice,retailPrice,images,quantity,categeory,defaultcategeory,width,height,depth,weight,shopprice):
    self.id = id
    self.name = name
    self.sku = sku
    self.url = url
    self.ean13 = ean13
    self.description = description
    self.tags = tags
    self.wholesalePrice = wholesalePrice
    self.retailPrice = "0"
    self.images = images
    self.quantity = quantity
    self.categeory = categeory
    self.defaultcategeory = defaultcategeory
    self.width = width
    self.height = height
    self.depth = depth
    self.weight = weight
    self.price = shopprice
    self.upc = ""
    self.active = "1"
    self.visiblity = "both"
    self.condition = "new"
    self.avilableForOrder ="1"
    self.showPrice = "1"
    self.avilableOnlineOnly = "0"
    self.shortDes = description
    self.specialPrice = round( shopprice-(shopprice/10)  ,2 )
    self.specialPriceSD ="2020-02-02"
    self.specialPriceED = "2022-02-02"
    self.OnSale = "1"
    self.metatitle = name
    self.metadec = name
    self.outOfStock = "0"
    self.minimimQuantity = "1"
    self.avilableDate = "2016-05-05"
    self.textInStock = "In Stock"
    self.textBackOrder = "Current Supply. Ordering Avilable"
    self.shipmentfee = ""
    self.feature = ""

