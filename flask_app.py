from flask import request
from flask import json
from flask import Flask
import sqlite3 as sql
import pymongo

app = Flask('yes')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["companydb"]
mycol = mydb["companies"]
print(myclient.list_database_names())
print(mydb.list_collection_names())

# connection = sqlite3.connect('semos_company_names.db')


@app.route('/get_comp', methods=['GET'])
def get_company():
    comp_id = request.args.get('id')
    try:
        with sql.connect("semos_company_names.db") as connection:
            comp_id = int(comp_id)
            cursor = connection.cursor()
            company = None
            cursor.execute("SELECT * FROM companies WHERE id=?", (comp_id,))
            rows = cursor.fetchall()
            for row in rows:
                company = row
            obj = {"id": company[0], "name": company[1],"country_iso": company[2], "city": company[3], "nace": company[4], "website": company[5] }
            response = app.response_class(  # konstruirame odgovor (response)
                response=json.dumps(obj),  # vo JSON format
                status=200,  # HTTP STATUS 200, succesful
                mimetype='application/json'  # tipot na povraten odgovor e vo JSON format
            )
            return response  # go vrakjame odgovorot
    except ValueError:
        return "id must be a number: "  + str(comp_id), 400
    except KeyError:
        return "id doesn't exist", 400

@app.route('/add_comp', methods=['POST'])
def add_comp():
    comp_data = json.loads(request.data)
    comp_id = comp_data['id'] 
    comp_name = comp_data['name']
    comp_c_iso = comp_data['country_iso'] 
    comp_city = comp_data['city']
    comp_nace = comp_data['nace']
    comp_web = comp_data['website']
    try:
        comp_id=int(comp_id) 
        comp = mycol.insert_one(comp_data)
        x = mycol.find_one(filter={"id":comp_id})
        print(x)
        return f"Company {comp_name} successfully added.", 200 #vrakjame string za uspesen zapis so HTTP STATUS 200	
    except ValueError:
        return "comp_id must be a number", 400 #vrakjame string kako odgovor so HTTP STATUS 400, ERROR

app.run(host='127.0.0.1', port = 5000)
