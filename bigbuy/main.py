from bigbuy import *

import json, csv

images = productsImages()
prod = products()
info = productsInformation()
stock = productsStock()

print("Pullling Images Data...")
images.pullData()
print("Completed\n")
print("Pulling products Data ...")
prod.pullData()
print("Completed \n")
print("Pulling Products additional information data...")
info.pullData()
print("Completed\n")
print("Pulling Stock data...")
stock.pullData()
print("Completed\n")


inf = info.read()

products = []

for value in inf:
	try:
		tempst = stock.getDataById(value['id'])
		if tempst == 0:
			continue
		tempi = images.getDataById(value['id'])
		tempp = prod.getDataById(value['id'])
		tempst = stock.getDataById(value['id'])
		products.append(finalProducts(value['id'],value['name'],value['sku'],value['url'],tempp['ean13'],value['description'],value['name'],tempp['wholesalePrice'],tempp['retailPrice'],tempi,tempst,tempp['category'],tempp['category'],tempp['width'],tempp['height'],tempp['depth'],tempp['weight'],tempp['inShopsPrice']))
	except Exception as e:
		print(1)
	
json_string = json.dumps([ob.__dict__ for ob in products])
jsonfile = open("jsondataall.json","w",encoding="utf-8")
jsonfile.write(json_string)
jsonfile.close()

count=0;
with open('finalproducts.csv', 'w', newline='', encoding="utf-8") as csvfile:
	spamwriter = csv.writer(csvfile)
	for pr in products:
		if count == 0:
			spamwriter.writerow(["ID","Name *","Reference #*","Price*","Friendly-url*","Ean-13","UPC","Active(0/1)","visibility(both/catalog/search/none)","Condition(new/used/refurbished)","Available for order (0 = No /1 = Yes)","Show Price","Available online only (0 = No/ 1 = Yes)",	"Short Description",	"Description",	"Tags(xâ€”y--z..)","Wholesale Price","Unit price","Special Price","special price start date","Special Price End Date","On sale (0/1)","Meta Title","Meta Description","Image Url(xâ€”y--z..)","Quantity","Out of stock","Minimal Quantity","Product available date","Text when in stock","Text when backorder allowed","Category Id(x--y--z..)","Default Category id","Width","height","depth","weight","Additional shipping cost","feature(Name:Value)"])
			spamwriter.writerow([0,pr.name,pr.sku,pr.price,pr.url,pr.ean13,pr.upc,pr.active,pr.visiblity,pr.condition,pr.avilableForOrder,1,pr.avilableOnlineOnly,pr.shortDes,pr.description,pr.tags,pr.wholesalePrice,pr.retailPrice,pr.specialPrice,pr.specialPriceSD,pr.specialPriceED,pr.OnSale,pr.metatitle,pr.metadec,pr.images,pr.quantity,pr.outOfStock,pr.minimimQuantity,pr.avilableDate,pr.textInStock,pr.textBackOrder,pr.categeory,pr.defaultcategeory,pr.width,pr.height,pr.depth,pr.weight,pr.shipmentfee,pr.feature])
			count = count+1
		else:
			spamwriter.writerow([0,pr.name,pr.sku,pr.price,pr.url,pr.ean13,pr.upc,pr.active,pr.visiblity,pr.condition,pr.avilableForOrder,1,pr.avilableOnlineOnly,pr.shortDes,pr.description,pr.tags,pr.wholesalePrice,pr.retailPrice,pr.specialPrice,pr.specialPriceSD,pr.specialPriceED,pr.OnSale,pr.metatitle,pr.metadec,pr.images,pr.quantity,pr.outOfStock,pr.minimimQuantity,pr.avilableDate,pr.textInStock,pr.textBackOrder,pr.categeory,pr.defaultcategeory,pr.width,pr.height,pr.depth,pr.weight,pr.shipmentfee,pr.feature])


print("Completed")