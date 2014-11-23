from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask import Flask, request, render_template, flash

import uuid

import config

Base = declarative_base()

class Zipcode(Base):
	__tablename__ = "zipcodes"
	id = Column(Integer, primary_key=True)
	code = Column(Integer, unique=True)
	lat_deg = Column(Integer)
	lat_min = Column(Integer)
	lat_sec = Column(Float)
	lon_deg = Column(Integer)
	lon_min = Column(Integer)
	lon_sec = Column(Float)

engine = create_engine(config.db)
Base.metadata.create_all(engine)

session = sessionmaker()
session.configure(autoflush=True, autocommit=False, bind=engine)
db = session()

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == "GET":
		return render_template('index.html', loc=None)
	else:
		if request.form['domain_name'] == "" and request.form['zip_code'] == "":
			flash('At least the zip code is required.')
			return render_template('index.html', loc=None)
		z = db.query(Zipcode).filter(Zipcode.code==request.form['zip_code']).first()
		if z:
			if request.form['domain_name'] == "":
				loc = "@\t86400\tIN\tLOC\t"+str(abs(z.lat_deg))+" "+str(z.lat_min)+" "+str(z.lat_sec)
			else:
				loc = request.form['domain_name']+".\t86400\tIN\tLOC\t"+str(abs(z.lat_deg))+" "+str(z.lat_min)+" "+str(z.lat_sec)
			if z.lat_deg >= 0:
				loc += " N "
			else:
				loc += " S "
			loc += str(abs(z.lon_deg))+" "+str(z.lon_min)+" "+str(z.lon_sec)
			if z.lon_deg >= 0:
				loc += " E "
			else:
				loc += " W "
			loc += "0.00m 0.00m 0.00m 0.00m"
			return render_template('index.html', loc="; here's your LOC record for "+request.form['zip_code']+"\n"+loc)
		else:
			flash('Invalid zip code')
			return render_template('index.html', loc=None)

if __name__ == "__main__":
	app.debug = True
	app.run()