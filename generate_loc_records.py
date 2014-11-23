import csv
import urllib.request

from web import Zipcode, db

def deg_to_dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = round((md - m) * 60, 2)
    if sd == 60.0:
    	sd -= 1
    return [d, m, sd]

##########################################################
# Populate database with code + lat/lon (in deg min sec) #
##########################################################

def populate(filename=None):
	if filename:
		with open(filename) as f:
			csv_file = f.readlines()
	else:
		csv_file = urllib.request.urlopen('http://federalgovernmentzipcodes.us/free-zipcode-database-Primary.csv').readlines()
		csv_file = [f.decode('utf-8') for f in csv_file]

	zipreader = csv.reader(csv_file, delimiter=',', quotechar='"')

	for i, row in enumerate(zipreader):
		if i == 0:
			continue
		if not row[0] == "" and not row[5] == "" and not row[6] == "":
			code = row[0]
			lat = deg_to_dms(float(row[5]))
			lon = deg_to_dms(float(row[6]))
			entry = Zipcode(code=code, lat_deg=lat[0], lat_min=lat[1], lat_sec=lat[2], lon_deg=lon[0], lon_min=lon[1], lon_sec=lon[2])
			db.add(entry)
			db.commit()

###############################################
# Generate DNS LOC records for every zip code #
###############################################

def generate_loc(domain, stub_output):
	zips = db.query(Zipcode).all()
	output = []
	for z in zips:
		record = str(z.code)+"."+domain+". 86400 IN LOC "+str(abs(z.lat_deg))+" "+str(z.lat_min)+" "+str(z.lat_sec)
		if z.lat_deg >= 0:
			record += " N "
		else:
			record += " S "
		record += str(abs(z.lon_deg))+" "+str(z.lon_min)+" "+str(z.lon_sec)
		if z.lon_deg >= 0:
			record += " E "
		else:
			record += " W "
		record += "0.00m 0.00m 0.00m 0.00m"
		output.append(record)
	with open(stub_output, 'w+t') as f:
		f.write("\n".join(output)+"\n")

# populate(filename='free-zipcode-database-Primary.csv')
generate_loc('ziptoloc.net', 'records.stub')