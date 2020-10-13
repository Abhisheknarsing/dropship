from flask import *
import logging
from logging import Formatter, FileHandler
import os
import csv, json
from bigbuy import finalProducts


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




@app.route('/assignCategeory')
def assign():
    filename = request.args.get('filename')
    fi = open("bigbuyData/files/config/"+str(filename)+".json","r")
    dat = fi.read()
    lister = dat.split(",")
    f = open("bigbuyData/products_got_from_bigbuy.json","r")
    data = json.loads(f.read())
    f.close()
    finaldata = []
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
                    if str(value['categeory']) == str(x.split(":")[0]):
                        if c == 0:
                            print(value['id'])
                            spamwriter.writerow(["ID","Name *","Reference #*","Price*","Friendly-url*","Ean-13","UPC","Active(0/1)","visibility(both/catalog/search/none)","Condition(new/used/refurbished)","Available for order (0 = No /1 = Yes)","Show Price","Available online only (0 = No/ 1 = Yes)",	"Short Description",	"Description",	"Tags(xâ€”y--z..)","Wholesale Price","Unit price","Special Price","special price start date","Special Price End Date","On sale (0/1)","Meta Title","Meta Description","Image Url(xâ€”y--z..)","Quantity","Out of stock","Minimal Quantity","Product available date","Text when in stock","Text when backorder allowed","Category Id(x--y--z..)","Default Category id","Width","height","depth","weight","Additional shipping cost","feature(Name:Value)"])
                            spamwriter.writerow([0,value['name'],value['sku'],value['price'],value['url'],value['ean13'],value['upc'],value['active'],value['visiblity'],value['condition'],value['avilableForOrder'],1,value['avilableOnlineOnly'],value['shortDes'],value['description'],value['tags'],value['wholesalePrice'],value['retailPrice'],value['specialPrice'],value['specialPriceSD'],value['specialPriceED'],value['OnSale'],value['metatitle'],value['metadec'],value['images'],value['quantity'],value['outOfStock'],value['minimimQuantity'],value['avilableDate'],value['textInStock'],value['textBackOrder'],x.split(":")[1],x.split(":")[1],value['width'],value['height'],value['depth'],value['weight'],value['shipmentfee'],value['feature']])
                            c = 3
                        else:
                            spamwriter.writerow([0,value['name'],value['sku'],value['price'],value['url'],value['ean13'],value['upc'],value['active'],value['visiblity'],value['condition'],value['avilableForOrder'],1,value['avilableOnlineOnly'],value['shortDes'],value['description'],value['tags'],value['wholesalePrice'],value['retailPrice'],value['specialPrice'],value['specialPriceSD'],value['specialPriceED'],value['OnSale'],value['metatitle'],value['metadec'],value['images'],value['quantity'],value['outOfStock'],value['minimimQuantity'],value['avilableDate'],value['textInStock'],value['textBackOrder'],x.split(":")[1],x.split(":")[1],value['width'],value['height'],value['depth'],value['weight'],value['shipmentfee'],value['feature']])
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

    fi = open("bigbuyData/files/config/"+str(filename)+".json","r")
    datatemp = fi.read()
    fi.close()

    fi = open("bigbuyData/files/config/"+str(filename)+".json","w+")
    fi.write(datatemp+','+str(pid)+':'+catname)
    fi.close()
    return "Success"




@app.route('/dashboard')
def dash():
    if not session.get('login'):
       return redirect("/", code=302)
    filename = request.args.get('seller')
    return render_template('pages/placeholder.dashboard.html',info=[filename])
    




@app.route('/pullData')
def pulldata():
    
    return "Success"

@app.route('/download')
def download():
    filename = request.args.get('filename')
    return send_from_directory(directory="bigbuyData/files", filename=str(filename)+".csv")

@app.route('/addCard')
def addCard():
    filename = request.args.get('filename')
    select = request.args.get('select')
    catID = request.args.get('zero')
    fi = open("bigbuyData/files/config/"+str(filename)+".json","w+")
    fi.write(catID)
    fi.close()
    pro = getjsonbyId(select)
    return render_template('pages/placeholder.firstcat.html',info=[filename],maindata=app.catdata, products=pro)



@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


file = open("bigbuyData/categeories.txt","r")
app.catdata=file.read()
app.catdata=json.loads(app.catdata)
file.close()

def getjsonbyId(idn):
    ran_list_to_save = []
    with open('bigbuyData/products_got_from_bigbuy.json') as f:
        tdata = json.load(f)
    for x in tdata:
        if str(x['defaultcategeory']) == str(idn):
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

