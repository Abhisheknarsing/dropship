from flask import *
import logging
from logging import Formatter, FileHandler
from forms import *
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
            return render_template('pages/placeholder.home.html',result="Wrong Password")
    return render_template('pages/placeholder.home.html')


@app.route('/seller')
def sellers():
    if not session.get('login'):
       return redirect("/", code=302)
    return render_template('pages/placeholder.seller.html')


@app.route('/openSeller')
def openseller():
    unique_list=[]
    finallist = []
    select = request.args.get('select')
    for x in app.catdata:
        if x['parentCategory'] not in unique_list:
            unique_list.append(x['parentCategory'])
    for x in unique_list:
        for b in app.catdata:
            if b['id'] == x:
                finallist.append([b['id'],b['name']])
    pro = getjsonbyId(select)
    print(pro)
    return render_template('pages/placeholder.catselector.html',result = finallist,maindata=app.catdata, products=pro)

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

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


file = open("datafiles/data.txt","r")
app.catdata=file.read()
app.catdata=json.loads(app.catdata)
file.close()

def getjsonbyId(idn):

    ran_list_to_save = []

    with open('datafiles/jsondataall.json') as f:
        tdata = json.load(f)
    
    for x in tdata:
        if str(x['defaultcategeory']) == str(idn):
            ran_list_to_save.append(x)
            
   
    return ran_list_to_save



if __name__ == '__main__':
    app.run()

