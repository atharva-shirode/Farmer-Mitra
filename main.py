import json
import pandas as pd
import numpy as np
import pickle
from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = "hello"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers.sqlite3'
app.config["SQLACLHEMY_TRACK_MODIFICATIONS"] = False


with open('bajra_model', 'rb') as f1:
    Bajra = pickle.load(f1)

with open('rice_model', 'rb') as f2:
    Rice = pickle.load(f2)

with open('wheat_model', 'rb') as f3:
    Wheat = pickle.load(f3)

with open('jowar_model', 'rb') as f4:
    Jowar = pickle.load(f4)

with open('groundnut_model', 'rb') as f5:
    Groundnut = pickle.load(f5)

with open('cotton_model', 'rb') as f6:
    Cotton = pickle.load(f6)

Bajra_Dist = {"Ahmednagar":100, "Akola":19, "Amarawati":61, "Aurangabad":99, "Beed":77,
       "Buldhana":92, "Dhule":80, "Jalna":100, "Jalgaon":106, "Mumbai":54, "Nandurbar":78,
       "Osmanabad":67, "Parbhani":35, "Pune":60, "Raigad":44, "Sangli":55, "Satara":42,
       "Sholapur":49, "Thane":53}

Rice_Dist = { 'Akola': 15, 'Beed': 9, 'Latur': 4 , 'Nanded': 40, 'Osmanabad': 13, 'Mumbai' : 51,
       'Raigad' : 80, 'Thane' : 80, 'Gadchiroli' : 14 , 'Nagpur' : 80 , 'Jalgaon' : 17, 'Nandurbar' : 38,
       'Nashik' : 80 , 'Pune' : 80 , 'Sangli' : 80 , 'Satara' : 17, 'Sholapur' : 80
}

Wheat_Dist = { 'Akola' : 80 , 'Amravati' : 80 , 'Buldhana' : 80 , 'Aurangabad' : 80 , 'Beed' : 80 , 'Nanded' : 80 ,
       'Mumbai' : 80 , 'Raigad' : 80 , 'Thane' : 80 , 'Bhandara' : 80 , 'Nagpur' : 80 , 'Wardha' : 80,
       'Dhule' : 80 , 'Jalgaon' : 80 , 'Nandurbar' : 80, 'Nashik' : 80 , 'Pune' : 80 , 'Sangli' : 80,
       'Sholapur' : 80
}

Groundnut_Dist = {
        'Ahmednagar' : 80 , 'Akola' : 4 , 'Amarawati' : 80 , 'Aurangabad' : 80 , 'Beed' : 44,
       'Buldhana' : 57 , 'Dhule' : 80 , 'Gadchiroli' : 48 , 'Hingoli' : 80 , 'Jalgaon' : 80 , 'Latur' : 64,
       'Mumbai' : 7 , 'Nandurbar' : 80 , 'Nagpur' : 80 , 'Nanded' : 80 , 'Nashik' : 74 , 'Osmanabad' : 57 ,
       'Parbhani' : 80 , 'Pune' :79  , 'Raigad' : 5 , 'Sholapur' : 80 , 'Vashim' : 80 , 'Wardha' : 41,
       'Yavatmal' : 80
}

Cotton_Dist = { 'Ahmednagar' : 29  , 'Akola' : 80 , 'Amarawati' : 80 , 'Aurangabad' : 90 , 'Beed' : 80,
       'Buldhana' : 80 , 'Chandrapur' : 80 , 'Dhule' : 80 , 'Gadchiroli' : 36, 'Hingoli' : 80,
       'Jalana' : 80, 'Jalgaon' : 80, 'Nagpur' : 80 , 'Nanded' : 80 , 'Nandurbar' : 80 , 'Parbhani' : 80,
       'Vashim' : 33 , 'Wardha' : 80 , 'Yavatmal' : 80
}

Jowar_Dist = {'Akola': 80 , 'Ahmednagar' : 74 , 'Amarawati' : 80 , 'Aurangabad' : 80 ,  'Beed' : 80,
       'Buldhana' : 80 , 'Chandrapur' : 9 , 'Dhule' : 80 , 'Hingoli' : 81, 'Jalana' : 80 , 'Jalgaon' : 80,
       'Latur' : 80 , 'Mumbai' : 80 , 'Nagpur' : 80 , 'Nanded' : 80 , 'Nandurbar' : 80 , 'Nashik': 80,
       'Osmanabad' : 58 , 'Parbhani' : 80 , 'Pune' : 80 , 'Raigad' : 80 , 'Sangli' : 63 , 'Satara' : 80,
       'Sholapur' : 80 , 'Thane' : 80 , 'Vashim' : 80 , 'Wardha' : 14, 'Yavatmal' : 80

}

rainfall = {
    "Ahmednagar" : 60 ,"Akola" : 80, "Amarawati" : 80.8, "Aurangabad":40, "Beed":69.2,
       "Buldhana":94.6, "Dhule":67.4, "Jalna":72, "Jalgaon":80, "Mumbai":90, "Nandurbar":80,
       "Osmanabad":73, "Parbhani":88.8, "Pune": 76 , "Raigad":90, "Sangli": 63.7, "Satara": 47.3 ,
       "Sholapur": 54.5, "Thane":90, "Nanded": 90, "Yawatmal" : 90, "Washim" : 95,"Kolhapur": 95, "Nagpur":60
}

temperature = {
        "Ahmednagar" : 25.75 ,"Akola" : 28.45, "Amarawati" : 27.75, "Aurangabad":26.12, "Beed": 26.12,
       "Buldhana": 28.62, "Dhule": 26.37, "Jalna": 26.4, "Jalgaon": 27.2, "Mumbai": 27.75, "Nandurbar": 25,
       "Osmanabad":28.9 , "Parbhani": 26.62, "Pune": 25.52 , "Raigad":29.5 , "Sangli": 25.12, "Satara": 23.85 ,
       "Sholapur": 27.37, "Thane":27.52, "Nanded": 28.62, "Yawatmal" : 27.25, "Washim" : 29 ,"Kolhapur":24.5 , "Nagpur":28.62

}

__data_columns = None
with open("columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']

wheat1 = None
with open("wheat_columns.json", "r") as f:
    wheat1 = json.load(f)['data_columns']

rice1 = None
with open("rice_columns.json", "r") as f:
    rice1 = json.load(f)['data_columns']

cotton1 = None
with open("cotton_columns.json", "r") as f:
    cotton1 = json.load(f)['data_columns']

jowar1 = None
with open("jowar_columns.json", "r") as f:
    jowar1 = json.load(f)['data_columns']

groundnut1 = None
with open("groundnut_columns.json", "r") as f:
    groundnut1 = json.load(f)['data_columns']

db = SQLAlchemy(app)

class farmers(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    Name = db.Column(db.String(200))
    Description = db.Column(db.String(500))
    Expenses = db.Column(db.Integer)
    Mode = db.Column(db.String(50))

    def __init__(self, Name, Description, Expenses, Mode):
        self.Name = Name
        self.Description = Description
        self.Expenses = Expenses
        self.Mode = Mode


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/price")
def price():
    return render_template("price.html")



@app.route("/predict_predict", methods=['POST'])
def predict_price():
    crop = request.form["crop"]
    district1 = request.form["district"]
    district  = request.form["district"]
    district = 'district_' + district
    mylist = []
    today = datetime.date.today()
    mylist.append(today)
    date = str(mylist[0])

    if crop == 'Bajra' :
        if district1 in Bajra_Dist:
            days = Bajra_Dist[district1]
            loc_index = __data_columns.index(district.lower())
            x = np.zeros(len(__data_columns))
            x[0] = days + 1
            x[loc_index] = 1
            price1= str(Bajra.predict([x])[0])
            output = 'Predicted price for next 7 days from '+date +' for '+crop+' in '+district1+' is Rs.'+price1
            return render_template('price.html', output= output)
        else:
            return render_template('price.html', output='No data available for '+district1+' district')
    elif crop == 'Rice' :
        if district1 in Rice_Dist:
            days = Rice_Dist[district1]
            loc_index = rice1.index(district.lower())
            x = np.zeros(len(rice1))
            x[0] = days + 1
            x[loc_index] = 1

            price2= str(Rice.predict([x])[0])
            return render_template('price.html', output='Predicted price for next 7 days from '+date +' for  '+crop+' in '+district1+' is Rs.'+price2)
        else:
            return render_template('price.html', output='No data available for '+district1+' district')
    elif crop == 'Wheat':
        if district1 in Wheat_Dist:
            days = Wheat_Dist[district1]
            loc_index = wheat1.index(district.lower())
            x = np.zeros(len(wheat1))
            x[0] = days + 1
            x[loc_index] = 1

            price3 = str(Wheat.predict([x])[0])
            return render_template('price.html',output='Predicted price for next 7 days from '+date +' for ' + crop + ' in ' + district1 + ' is Rs.' + price3)
        else:
            return render_template('price.html', output='No data available for ' + district1 + ' district')
    elif crop == 'Jowar' :
        if district1 in Jowar_Dist:
            days = Jowar_Dist[district1]
            loc_index = jowar1.index(district.lower())
            x = np.zeros(len(jowar1))
            x[0] = days + 1
            x[loc_index] = 1

            price4 = str(Jowar.predict([x])[0])
            return render_template('price.html',output='Predicted price for next 7 days from '+date +' for ' + crop + ' in ' + district1 + ' is Rs.' + price4)
        else:
            return render_template('price.html', output='No data available for ' + district1 + ' district')
    elif crop == 'Groundnut' :
        if district1 in Groundnut_Dist:
            days = Groundnut_Dist[district1]
            loc_index = groundnut1.index(district.lower())
            x = np.zeros(len(groundnut1))
            x[0] = days + 1
            x[loc_index] = 1

            price5 = str(Groundnut.predict([x])[0])
            return render_template('price.html',output='Predicted price for next 7 days from '+date +' for ' + crop + ' in ' + district1 + ' is Rs.' + price5)
        else:
            return render_template('price.html', output='No data available for ' + district1 + ' district')
    elif crop == 'Cotton' :
        if district1 in Cotton_Dist:
            days = Cotton_Dist[district1]
            loc_index = cotton1.index(district.lower())
            x = np.zeros(len(cotton1))
            x[0] = days + 1
            x[loc_index] = 1

            price6 = str(Cotton.predict([x])[0])
            return render_template('price.html',output='Predicted price for next 7 days from '+date +' for ' + crop + ' in ' + district1 + ' is Rs.' + price6)
        else:
            return render_template('price.html', output='No data available for ' + district1 + ' district')


@app.route("/yield_predict",methods=['POST','GET'])
def yield_predict():
    if request.method == "POST":
            district2 = request.form["district"]
            crop1 = request.form["crop"]
            ph = float(request.form["ph"])
            dist_temp = temperature[district2]
            dist_rainfall = rainfall[district2]

            if crop1 == 'Bajra':
                return render_template('bajra.html',district2=district2,dist_temp=dist_temp,dist_rainfall=dist_rainfall,ph=ph)
            elif crop1 == 'Rice':
                return render_template('rice.html',district2=district2,dist_temp=dist_temp,dist_rainfall=dist_rainfall,ph=ph)
            elif crop1 == 'Wheat':
                return render_template('wheat.html',district2=district2,dist_temp=dist_temp,dist_rainfall=dist_rainfall,ph=ph)
            elif crop1 == 'Groundnut':
                return render_template('groundnut.html',district2=district2,dist_temp=dist_temp,dist_rainfall=dist_rainfall,ph=ph)
            elif crop1 == 'Cotton':
                return render_template('cotton.html',district2=district2,dist_temp=dist_temp,dist_rainfall=dist_rainfall,ph=ph)
            elif crop1 == 'Jowar':
                return render_template('jawar.html',district2=district2,dist_temp=dist_temp,dist_rainfall=dist_rainfall,ph=ph)

    else:
        return render_template('yield_predict.html')

@app.route("/bajra")
def bajra():
    render_template("bajra.html")

@app.route("/rice")
def rice():
    render_template("rice.html")

@app.route("/wheat")
def wheat():
    render_template("wheat.html")

@app.route("/groundnut")
def groundnut():
    render_template("groundnut.html")

@app.route("/cotton")
def cotton():
    render_template("cotton.html")

@app.route("/jawar")
def jawar():
    render_template("jawar.html")

@app.route("/layout")
def layout():
    render_template("layout.html")

@app.route("/view")
def view():
    return render_template("view.html", values=farmers.query.all())


@app.route("/Task", methods=["POST", "GET"])
def Task():
    if request.method == "POST":

        if not request.form['Name'] or not request.form['Description'] or not request.form['Expenses'] or not \
        request.form['Mode']:
            flash('Please enter all the fields', 'error')
        else:
            farmer = farmers(request.form['Name'], request.form['Description'],
                             request.form['Expenses'], request.form['Mode'])

            db.session.add(farmer)
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for("view"))
    return render_template("Task.html")


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        z = request.form['Name']
        x = db.session.query(farmers).filter(farmers.Name == z).first()

        db.session.delete(x)
        db.session.commit()

        flash('Record was successfully deleted')
        return redirect(url_for("delete"))
    return render_template("delete.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
