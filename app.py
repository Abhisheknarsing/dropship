from flask import *
import logging
from logging import Formatter, FileHandler
import os
import csv, json


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
    return dat




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

    fi = open("bigbuyData/files/config/"+str(filename)+".json","r")
    datatemp = fi.read()
    fi.close()

    fi = open("bigbuyData/files/config/"+str(filename)+".json","w+")
    fi.write(datatemp+','+str(pid))
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

@app.route('/downloadCatCSV')
def download():
    filename = request.args.get('filename')
    catID = request.args.get('catID')
    return str(catID)+str(filename)

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

