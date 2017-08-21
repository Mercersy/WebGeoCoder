from flask import Flask, render_template, request, send_file, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy as sqa
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from werkzeug import secure_filename
import os
os.environ["GOOGLE_API_KEY"] = ""
import geocoder
from pandas import DataFrame

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pSql1@localhost/address'
app.secret_key = 'sdjfgauogsadiushd'
db = sqa(app)
eng = create_engine('postgresql://postgres:pSql1@localhost/address')
conn = eng.connect()

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    address_ = db.Column(db.String(120), unique = True)
    company_ = db.Column(db.String(120))
    hc_ = db.Column(db.Integer)
    lon_ = db.Column(db.Float)
    lat_ = db.Column(db.Float)

    def __init__(self, address_, company_, hc_, lon_, lat_):
        self.address_ = address_
        self.company_ = company_
        self.hc_ = hc_
        self.lon_ = lon_
        self.lat_ = lat_

@app.route("/")
def index():
    if 'username' in session:
        return render_template("index.html")
    db.create_all()
    db.session.query(Data).delete()
    db.session.commit()
    return ("Welcome new user! <br><a href = '/login'></b>"+"click here to log in</b></a>")


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect("/")
    return render_template("login.html")

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route("/submit", methods = ['POST'])
def submit():
    if request.method == "POST":
        address = request.form["address_name"]
        company = request.form["company_name"]
        hc = request.form["hc_name"]
        if db.session.query(Data).filter(Data.address_ == address).count() == 0:
            g = geocoder.google(address)
            data = Data(address, company, hc, float(g.latlng[0]), float(g.latlng[1]))
            db.session.add(data)
            db.session.commit()
            return redirect("/")#, text = "Submitted!")
        return redirect("/")#, text = "Address already exists!")


@app.route("/clean", methods = ['POST'])
def clean():
    if request.method == "POST":
        db.session.query(Data).delete()
        db.session.commit()
        return redirect("/")

@app.route("/table", methods = ['POST'])
def show_table():
    if request.method == "POST":
        tmp = conn.execute("SELECT * from data")
        df = DataFrame(tmp.fetchall())
        df.columns = tmp.keys()
        return render_template("index.html", tables = [df.to_html()], titles = ["My Table"])


if __name__ == "__main__":
    app.debug = True
    app.run()
