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