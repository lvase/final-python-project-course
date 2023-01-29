from flask import request
from flask import json
from flask import Flask
import sqlite3 as sql

app = Flask('yes')

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
            response = app.response_class(  # konstruirame odgovor (response)
                response=json.dumps(company),  # vo JSON format
                status=200,  # HTTP STATUS 200, succesful
                mimetype='application/json'  # tipot na povraten odgovor e vo JSON format
            )
            return response  # go vrakjame odgovorot
    except ValueError:
        return "id must be a number: "  + str(comp_id), 400
    except KeyError:
        return "id doesn't exist", 400
