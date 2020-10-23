from flask import *
import logging
from logging import Formatter, FileHandler
import os
import csv, json
from bigbuy import *
import requests
import xlrd
import pandas as pd 
import numpy as np


app = Flask(__name__)

app.config.from_object('config')
app.password = "123"
app.url = "localhost"

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        if request.values.get('password') == app.password:
            session['login'] = True
            return redirect("/seller", code=302)
        else:
            return render_template('pages/placeholder.login.html',result="Wrong Password")
    return render_template('pages/placeholder.login.html')


@app.route('/seller')
def sellers():
    if not session.get('login'):
       return redirect("/", code=302)
    return render_template('pages/placeholder.seller.html')


@app.route('/openSeller')
def openseller():
    if not session.get('login'):
       return redirect("/", code=302)
    select = request.args.get('select')
    filename = request.args.get('filename')
    pro = getjsonbyId(select)
    return render_template('pages/placeholder.catselector.html',info=[filename,select],maindata=app.catdata, products=pro)


@app.route('/fetchdata')
def fetch():
    data = Bigbuy()
    data.pullAllData()
    return "success data imported successfully"




@app.route('/assignCategeory')
def assign():
    filename = request.args.get('filename')
    fi = open("bigbuyData/files/config/"+str(filename)+".json","r")
    dat = fi.read()
    fi.close()
    proremover = open("bigbuyData/files/"+str(filename)+"nopro"+".json","r")
    nopro = proremover.read()
    proremover.close()
    nopro = nopro.split(",")

    lister = dat.split(",")
    f = open("bigbuyData/products_got_from_bigbuy.json","r")
    data = json.loads(f.read())
    f.close()
    finaldata = []
    jsondata=[]
    count=0
    c=0
    zero = False
    with open('bigbuyData/files/'+str(filename)+'.csv', 'w+', newline='', encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile)
        for x in lister:
            if count == 0:
                count=2
                if str(x) == str("0"):
                    zero = True
            else:
                for value in data:
                    if str(value['categeory']) == str(x.split("---")[0]):
                        if zero:
                            if str(value['quantity']) == str(0):
                                continue
                        if str(value['id']) in nopro:
                            continue
                        tempjson = {}
                        tempjson['id'] = value['id']
                        tempjson['sku'] = value['sku']
                        tempjson['quantity'] = value['quantity']
                        jsondata.append(json.dumps(tempjson))
                        if c == 0:
                            spamwriter.writerow(["ID","Name *","Reference #*","Price*","Friendly-url*","Ean-13","UPC","Active(0/1)","visibility(both/catalog/search/none)","Condition(new/used/refurbished)","Available for order (0 = No /1 = Yes)","Show Price","Available online only (0 = No/ 1 = Yes)",	"Short Description",	"Description",	"Tags(xâ€”y--z..)","Wholesale Price","Unit price","Special Price","special price start date","Special Price End Date","On sale (0/1)","Meta Title","Meta Description","Image Url(xâ€”y--z..)","Quantity","Out of stock","Minimal Quantity","Product available date","Text when in stock","Text when backorder allowed","Category Id(x--y--z..)","Default Category id","Width","height","depth","weight","Additional shipping cost","feature(Name:Value)"])
                            spamwriter.writerow([0,value['name'],value['sku'],value['price'],value['url'],value['ean13'],value['upc'],value['active'],value['visiblity'],value['condition'],value['avilableForOrder'],1,value['avilableOnlineOnly'],value['shortDes'],value['description'], "".join(e for e in value['tags'].replace('"',"and") if e.isalnum()),value['wholesalePrice'],value['retailPrice'],value['specialPrice'],"2020-11-01","2020-12-31",value['OnSale'],value['metatitle'],value['metadec'],value['images'],value['quantity'],value['outOfStock'],value['minimimQuantity'],value['avilableDate'],value['textInStock'],value['textBackOrder'],str(x.split("---")[1]).split(":")[1],str(x.split("---")[1]).split(":")[0],value['width'],value['height'],value['depth'],value['weight'],value['shipmentfee'],value['feature']])
                            c = 3
                        else:
                            spamwriter.writerow([0,value['name'],value['sku'],value['price'],value['url'],value['ean13'],value['upc'],value['active'],value['visiblity'],value['condition'],value['avilableForOrder'],1,value['avilableOnlineOnly'],value['shortDes'],value['description'],"".join(e for e in value['tags'].replace('"',"and") if e.isalnum()),value['wholesalePrice'],value['retailPrice'],value['specialPrice'],"2020-11-01","2020-12-31",value['OnSale'],value['metatitle'],value['metadec'],value['images'],value['quantity'],value['outOfStock'],value['minimimQuantity'],value['avilableDate'],value['textInStock'],value['textBackOrder'],str(x.split("---")[1]).split(":")[1],str(x.split("---")[1]).split(":")[0],value['width'],value['height'],value['depth'],value['weight'],value['shipmentfee'],value['feature']])
    
    f = open('bigbuyData/files/'+str(filename)+'.json','w+')
    f.write(json.dumps(jsondata))
    f.close()
    return render_template('pages/download.html',info=[str(filename)])



@app.route('/add')
def add():
    session['filename'] = "something.json"
    filename = session.get('file')
    pid= request.args.get('pid')
    pid = getjsonbyProductId(pid)
    return str(pid)
    
@app.route('/addCat')
def addcat():
    filename = request.args.get('filename')
    pid= request.args.get('id')
    catname = request.args.get('categeory')
    pcatname = request.args.get('pcategeory')

    fi = open("bigbuyData/files/config/"+str(filename)+".json","r")
    datatemp = fi.read()
    fi.close()

    fi = open("bigbuyData/files/config/"+str(filename)+".json","w+")
    fi.write(datatemp+','+str(pid)+'---'+str(pcatname)+':'+catname)
    fi.close()
    return "Success"


@app.route('/deleteCard')
def delCard():
    filename = request.args.get('filename')
    os.remove(os.path.join("bigbuyData/files/config",filename))
    os.remove(os.path.join("bigbuyData/files",filename))
    os.remove(os.path.join("bigbuyData/files",filename.replace(".json","nopro.json")))
    os.remove(os.path.join("bigbuyData/files",filename.replace(".json",".csv")))
    return "Removed"

@app.route('/dashboard')
def dash():
    if not session.get('login'):
       return redirect("/", code=302)
    filename = request.args.get('seller')
    arr = os.listdir(os.path.join("bigbuyData/files/config"))

    return render_template('pages/placeholder.dashboard.html',info=[filename],arr = arr)

@app.route('/showcase')
def showcase():
    select = request.args.get('select')
    if select == None:
        select = 0
    pro = getjsonbyId(select)
    return render_template('pages/showcase.html',info=[select],maindata=app.catdata, products=pro)



@app.route('/track2')
def track2():
    filename = request.args.get('filename')
    f = open('bigbuyData/files/'+str(filename)+'.json','r',encoding="utf8")
    data = f.read()
    f.close()
    data = json.loads(data)
    

    f = open('bigbuyData/recCat.json','r',encoding="utf8")
    updated_stox = f.read()
    f.close()
    updated_stox = json.loads(updated_stox)
    changes = []

    for x in data:
        x = json.loads(x)
        
        for y in updated_stox:
            
            if str(x['id']) == str(y['id']):
                if str(x["quantity"]) != str(y["stocks"][0]["quantity"]):
                    if int(y["stocks"][0]["quantity"]) == 0:
                        changes.append([y['sku'],y["stocks"][0]["quantity"],x["quantity"]])
                    if int(x["quantity"]) == 0:
                        changes.append([y['sku'],y["stocks"][0]["quantity"],x["quantity"]])
    return render_template('pages/tracker.html',data=changes,filename=[filename])





@app.route('/download')
def download():
    filename = request.args.get('filename')
    return send_from_directory(directory="bigbuyData/files", filename=str(filename)+".csv",as_attachment=True)


@app.route('/downloadyts')
def downl():
    filename = request.args.get('filename')
    return send_from_directory(directory="yns/files", filename=str(filename)+".csv",as_attachment=True)



@app.route('/changeValue')
def change():
    sku = request.args.get('sku')
    q = request.args.get('quantity')
    filename = request.args.get('filename')
    f = open('bigbuyData/files/'+str(filename)+'.json','r',encoding="utf8")
    data = f.read()
    f.close()
    data = json.loads(str(data))
    new_list = []
    obj = {}
    for x in data:
        y= json.loads(x)
        obj['id'] = str(y['id'])
        obj['sku'] = str(y['sku'])
        if str(y['sku']) == str(sku):
            obj['quantity'] = q
        else:
            obj['quantity'] = str(y['quantity'])
        new_list.append(json.dumps(obj))
        obj = {}
    f = open('bigbuyData/files/'+str(filename)+'.json','w',encoding="utf8")
    f.write(json.dumps(new_list))
    f.close()

    return "success"


@app.route('/addCard')
def addCard():
    filename = request.args.get('filename')
    catID = request.args.get('zero')
    fi = open("bigbuyData/files/config/"+str(filename)+".json","w+")
    fi.write(catID)
    fi.close()
    proremover = open("bigbuyData/files/"+str(filename)+"nopro"+".json","w+")
    proremover.write("")
    proremover.close()
    return render_template('pages/placeholder.firstcat.html',info=[filename],maindata=app.catdata)


@app.route('/signout')
def signout():
    session.pop('login', None)
    return render_template('pages/placeholder.login.html')


@app.route('/removeProduct')
def removeP():
    filename = request.args.get('filename')
    proid = request.args.get('id')
    fi = open("bigbuyData/files/"+str(filename)+"nopro"+".json","r")
    existdata = fi.read()
    fi.close()
    if existdata == "":
        existdata = str(proid)
    else:
        existdata = existdata+","+str(proid)

    fi = open("bigbuyData/files/"+str(filename)+"nopro"+".json","w+")
    fi.write(existdata)
    fi.close()

    return "success"



@app.route('/reloadStock')
def reloadStox():
    bb = Bigbuy()
    bb.reloadCat()
    return "done"



# *****************************************************************************************************************************

@app.route('/yns')
def yns():
    arr = os.listdir(os.path.join("yns/files/config"))
    return render_template('pages/yournewstyle.html',arr=arr)


@app.route('/ynscatselector')
def ynscat():
    filename = request.args.get('filename')
    catID = request.args.get('zero')
    fi = open("yns/files/config/"+str(filename)+".json","w+")
    fi.write(catID)
    fi.close()
    proremover = open("yns/files/"+str(filename)+"nopro"+".json","w+")
    proremover.write("")
    proremover.close()
    
    return render_template('pages/ynsfirst.html',info=[filename],maindata=app.ytscat)


@app.route('/choosecat')
def choosecat():
    select = request.args.get('select')
    filename = request.args.get('filename')
    products = []
    for x in app.ytspro:
        if int(x['categeory']) == int(select):
            products.append(x)
    
    return render_template('pages/ytscatselector.html',info=[filename,select],maindata=app.ytscat, products=products)


@app.route('/addCatyns')
def addcatyns():
    filename = request.args.get('filename')
    pid= request.args.get('id')
    catname = request.args.get('categeory')
    pcatname = request.args.get('pcategeory')

    fi = open("yns/files/config/"+str(filename)+".json","r")
    datatemp = fi.read()
    fi.close()

    fi = open("yns/files/config/"+str(filename)+".json","w+")
    fi.write(datatemp+','+str(pid)+'---'+str(pcatname)+':'+catname)
    fi.close()
    return "Success"


@app.route('/removeProductyns')
def removePyns():
    filename = request.args.get('filename')
    proid = request.args.get('id')
    fi = open("yns/files/"+str(filename)+"nopro"+".json","r")
    existdata = fi.read()
    fi.close()
    if existdata == "":
        existdata = str(proid)
    else:
        existdata = existdata+","+str(proid)

    fi = open("yns/files/"+str(filename)+"nopro"+".json","w+")
    fi.write(existdata)
    fi.close()

    return "success"


@app.route('/assignCategeoryyns')
def assin():
    filename = request.args.get('filename')
    fi = open("yns/files/config/"+str(filename)+".json","r")
    dat = fi.read()
    fi.close()
    proremover = open("yns/files/"+str(filename)+"nopro"+".json","r")
    nopro = proremover.read()
    proremover.close()
    nopro = nopro.split(",")
    lister = dat.split(",")
    data = app.ytspro
    finaldata = []
    jsondata=[]
    count=0
    c=0
    zero = False
    with open('yns/files/'+str(filename)+'.csv', 'w+', newline='', encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile)
        for x in lister:
            if count == 0:
                count=2
                if str(x) == str("0"):
                    zero = True
            else:
                for value in data:
                    if str(value['categeory']) == str(x.split("---")[0]):
                        if str(value['id']) in nopro:
                            continue
                        tempjson = {}
                        tempjson['id'] = value['id']
                        tempjson['sku'] = value['id']
                        jsondata.append(json.dumps(tempjson))
                        if c == 0:
                            spamwriter.writerow(["ID","Name *","Reference #*","Price*","Friendly-url*","Ean-13","UPC","Active(0/1)","visibility(both/catalog/search/none)","Condition(new/used/refurbished)","Available for order (0 = No /1 = Yes)","Show Price","Available online only (0 = No/ 1 = Yes)",	"Short Description",	"Description",	"Tags(xâ€”y--z..)","Wholesale Price","Unit price","Special Price","special price start date","Special Price End Date","On sale (0/1)","Meta Title","Meta Description","Image Url(xâ€”y--z..)","Quantity","Out of stock","Minimal Quantity","Product available date","Text when in stock","Text when backorder allowed","Category Id(x--y--z..)","Default Category id","Width","height","depth","weight","Additional shipping cost","feature(Name:Value)"])
                            spamwriter.writerow([0,value['name'],value['id'],value['price'],"","","",1,"both","new",1,1,0,value['description'],value['description'], "".join(e for e in value['name'].replace('"',"and") if e.isalnum()),value['WholesalePrice'],value['price'],value['price'],"2020-11-01","2020-12-31",1,value['name'],value['name'],value['images'],0,0,1,"2020-05-05","In Stock","current Supply, ordering avilabel",str(x.split("---")[1]).split(":")[1],str(x.split("---")[1]).split(":")[0],10,10,10,2,"",""])
                            c = 3
                        else:
                            spamwriter.writerow([0,value['name'],value['id'],value['price'],"","","",1,"both","new",1,1,0,value['description'],value['description'], "".join(e for e in value['name'].replace('"',"and") if e.isalnum()),value['WholesalePrice'],value['price'],value['price'],"2020-11-01","2020-12-31",1,value['name'],value['name'],value['images'],0,0,1,"2020-05-05","In Stock","current Supply, ordering avilabel",str(x.split("---")[1]).split(":")[1],str(x.split("---")[1]).split(":")[0],10,10,10,2,"",""])
    f = open('yns/files/'+str(filename)+'.json','w+')
    f.write(json.dumps(jsondata))
    f.close()
    return render_template('pages/downloadyts.html',info=[str(filename)])


@app.route('/deleteCardyts')
def delCardyts():
    filename = request.args.get('filename')
    os.remove(os.path.join("yns/files/config",filename))
    os.remove(os.path.join("yns/files",filename))
    os.remove(os.path.join("yns/files",filename.replace(".json","nopro.json")))
    os.remove(os.path.join("yns/files",filename.replace(".json",".csv")))
    return "Removed"

@app.route('/addCombinations')
def addCombinations():
    filename = request.args.get('filename')
    return render_template('pages/addcombinations.html',info=[str(filename)])

@app.route('/combi', methods=['POST'])
def addCombi():
    filename = request.values.get('filename')
    uploaded_file = request.files['csvfile']
    uploaded_file.save("yns/files/"+filename+"export.csv")
    combinations_file_name = "yns/comb.xls"
    exported_file_name = "yns/files/"+filename+"export.csv"
    f = open(exported_file_name,"r")
    data = f.read()
    f.close()
    data = data.replace(",","--")
    data = data.replace(";",",")
    data = data.replace("--",";")
    f = open("yns/"+filename+"newimport.csv","w+")
    data = f.write(data)
    f.close()
    df_new = pd.read_csv("yns/"+filename+"newimport.csv") 
    GFG = pd.ExcelWriter("yns/"+filename+"Names.xlsx")
    df_new.to_excel(GFG, index = False) 
    GFG.save()
    foundid = ""
    loc = (combinations_file_name)
    exported = ("yns/"+filename+"Names.xlsx")
    
    workbook = xlrd.open_workbook(exported)
    exportsheet = workbook.sheet_by_index(0)
    list_of_comb = []
    list_obj = {}
    tempcount = 0
    for x in range(exportsheet.nrows):
        if tempcount == 0:
            tempcount=1
            continue
        list_obj['Kid'] = int(exportsheet.row_values(x)[0])
        list_obj['Yid'] = int(exportsheet.row_values(x)[2])
        list_of_comb.append(list_obj)
        list_obj = {}
    c=0
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    images=""
    with open('yns/'+filename+'combinations.csv', 'w', newline='', encoding="utf-8") as csvi:
        spamwriter = csv.writer(csvi)
        spamwriter.writerow(["Product ID*","Attribute (Name:Value)*","Reference","EAN13","UPC*","Quantity","Combination avilable date","default(0/1)","image url","Delete Existing Images(0/1)"])
        for x in range(sheet.nrows):
            if c!=0:
                for temp in list_of_comb:
                    if str(temp['Yid']) == str(int(sheet.row_values(x)[0])):
                        foundid = str(temp['Kid'])
                        spamwriter.writerow([foundid,"Size:"+str(sheet.row_values(x)[2]).split(":")[0],sheet.row_values(x)[4],"","",int(sheet.row_values(x)[3]),"2020-05-05",0,"",0])
                        images=""
            else :
                c=c+1
            c=c+1
    return send_from_directory(directory="yns", filename='yns/'+filename+'combinations.csv',as_attachment=True)











#*********************************************************************************************************************************

f = open("yns/cat.txt","r",encoding='cp850')
k = f.read()
f.close()
app.ytscat = json.loads(k)

ytsfilename = ("yns/ppp.xls") 
count=0
img_count = 0
wb = xlrd.open_workbook(ytsfilename) 
sheet = wb.sheet_by_index(0) 
images_data=""
obj = {}
products_list = []
for x in range(sheet.nrows):
    if count!=0:
        try:
            for y in sheet.row_values(x)[9].split(","):
                if img_count == 0:
                    images_data = y
                else:
                    images_data = images_data+";"+y

                
            obj['id'] = int(sheet.row_values(x)[0])
            obj['name'] = sheet.row_values(x)[3]
            obj['price'] = sheet.row_values(x)[11]
            obj['categeory'] = int(sheet.row_values(x)[4])
            obj['images'] = images_data
            obj['description'] = sheet.row_values(x)[8]
            obj['WholesalePrice'] = sheet.row_values(x)[10]
            obj['netprice'] = sheet.row_values(x)[11]
            products_list.append(obj)
            obj = {}
            images_data=""
        except :
            pass
    else:
        count=count+1
    count=count+1
app.ytspro = products_list

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 400





file = open("bigbuyData/categeories.txt","r")
app.catdata=file.read()
app.catdata=json.loads(app.catdata)
file.close()

file = open("bigbuyData/products_got_from_bigbuy.json","r")
app.products=file.read()
app.products=json.loads(app.products)
file.close()

def getjsonbyId(catid):
    ran_list_to_save = []
    for x in app.products:
        if int(x['defaultcategeory']) == int(catid):
            ran_list_to_save.append(x)
    return ran_list_to_save

def getjsonbyProductId(idn):
    ran_list_to_save = ""
    with open('bigbuyData/products_got_from_bigbuy.json') as f:
        pdata = json.load(f)
    for y in pdata:
        if str(y['id']) == str(idn):
            return y
    return "none"

if __name__ == '__main__':
    app.run()

