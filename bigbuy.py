import requests, json, csv


class Bigbuy:

  def __init__(self):
    self.productsImagesData = None
    self.productsData = None
    self.productsInformationData = None
    self.productsStockData = None
    self.finalProductsData = None

  def reloadCat(self):
    endpoint = "https://api.bigbuy.eu/rest/catalog/productsstock.json?isoCode=en"
    temp_cat_data = requests.get(endpoint, headers= self.getAuthHeader()).json()
    f = open("bigbuyData/recCat.json","w+")
    f.write(json.dumps(temp_cat_data))
    f.close()


  def getAuthHeader(self):
    return {"Authorization": "Bearer NGFkMzI5NGIwMDM1ZmM2ODNkYTZmYTQ3Nzk3MjNjNDNlN2QwZGE5NWIyMjg1YWRkNDA0NzVkOTc1OTA0NTM1NA"}

  def pullAllData(self):
    self.productsImagesData = productsImages()
    self.productsInformationData = productsInformation()
    self.productsStockData = productsStock()
    self.productsData = productsMainInfo()
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

    inf = self.productsInformationData.read()
    products = []
    for value in inf:
    	try:
    		tempst = self.productsStockData.getDataById(value['id'])
    		tempi = self.productsImagesData.getDataById(value['id'])
    		tempp = self.productsData.getDataById(value['id'])
    		products.append(finalProducts(value['id'],value['name'],value['sku'],value['url'],tempp['ean13'],value['description'],value['name'],tempp['wholesalePrice'],tempp['retailPrice'],tempi,tempst,tempp['category'],tempp['category'],tempp['width'],tempp['height'],tempp['depth'],tempp['weight'],tempp['inShopsPrice']))
    	except Exception as e:
    		print("Not Found")
    json_string = json.dumps([ob.__dict__ for ob in products])
    jsonfile = open("bigbuyData/products_got_from_bigbuy.json","w",encoding="utf-8")
    jsonfile.write(json_string)
    jsonfile.close()
    count=0;
    with open('bigbuyData/products_got_from_bigbuy.csv', 'w', newline='', encoding="utf-8") as csvfile:
    	spamwriter = csv.writer(csvfile)
    	for pr in products:
    		if count == 0:
    			spamwriter.writerow(["ID","Name *","Reference #*","Price*","Friendly-url*","Ean-13","UPC","Active(0/1)","visibility(both/catalog/search/none)","Condition(new/used/refurbished)","Available for order (0 = No /1 = Yes)","Show Price","Available online only (0 = No/ 1 = Yes)",	"Short Description",	"Description",	"Tags(xâ€”y--z..)","Wholesale Price","Unit price","Special Price","special price start date","Special Price End Date","On sale (0/1)","Meta Title","Meta Description","Image Url(xâ€”y--z..)","Quantity","Out of stock","Minimal Quantity","Product available date","Text when in stock","Text when backorder allowed","Category Id(x--y--z..)","Default Category id","Width","height","depth","weight","Additional shipping cost","feature(Name:Value)"])
    			spamwriter.writerow([0,pr.name,pr.sku,pr.price,pr.url,pr.ean13,pr.upc,pr.active,pr.visiblity,pr.condition,pr.avilableForOrder,1,pr.avilableOnlineOnly,pr.shortDes,pr.description,pr.tags,pr.wholesalePrice,pr.retailPrice,pr.specialPrice,pr.specialPriceSD,pr.specialPriceED,pr.OnSale,pr.metatitle,pr.metadec,pr.images,pr.quantity,pr.outOfStock,pr.minimimQuantity,pr.avilableDate,pr.textInStock,pr.textBackOrder,pr.categeory,pr.defaultcategeory,pr.width,pr.height,pr.depth,pr.weight,pr.shipmentfee,pr.feature])
    			count = count+1
    		else:
    			spamwriter.writerow([0,pr.name,pr.sku,pr.price,pr.url,pr.ean13,pr.upc,pr.active,pr.visiblity,pr.condition,pr.avilableForOrder,1,pr.avilableOnlineOnly,pr.shortDes,pr.description,pr.tags,pr.wholesalePrice,pr.retailPrice,pr.specialPrice,pr.specialPriceSD,pr.specialPriceED,pr.OnSale,pr.metatitle,pr.metadec,pr.images,pr.quantity,pr.outOfStock,pr.minimimQuantity,pr.avilableDate,pr.textInStock,pr.textBackOrder,pr.categeory,pr.defaultcategeory,pr.width,pr.height,pr.depth,pr.weight,pr.shipmentfee,pr.feature])

class productsMainInfo:

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
    productslist = []
    for emp in self.data:
      productslist.append(Product(emp['id'],emp['sku'],emp['ean13'],emp['weight'],emp['height'],emp['width'],emp['depth'],emp['dateUpd'],emp['category'],emp['wholesalePrice'],emp['retailPrice'],emp['taxRate'],emp['taxId'],emp['inShopsPrice']))

    with open('products1.csv', 'w', newline='', encoding="utf-8") as csvfile:
      spamwriter = csv.writer(csvfile)
      for record in productslist:
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

