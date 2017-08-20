from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy as sqa
from sqlalchemy.sql import func
from werkzeug import secure_filename
import geocoder
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pSql1@localhost/address'

db = sqa(app)


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

@app.route("/", methods = ['GET'])
def index():
    db.create_all()
    db.session.query(Data).delete()
    db.session.commit()
    return render_template("index.html")

@app.route("/", methods = ['POST'])
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
            return render_template("index.html", text = "Submitted!")
        return render_template("index.html", text = "Address already exists!")


# def map():
#     return render_template("map.html")



if __name__ == "__main__":
    app.debug = True
    app.run()
