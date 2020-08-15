import os

from flask import Flask, render_template, flash, request, redirect, url_for, jsonify, make_response, after_this_request
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy

from Task import run

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Integer)
    monthly_budget = db.Column(db.Integer)
    distance_travelled = db.Column(db.Integer)
    fuel_price = db.Column(db.Integer)
    car_make = db.Column(db.String(100))
    average_per_litre = db.Column(db.Integer)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.form:
        total_budget = request.form['a']
        monthly_budget = request.form["b"]
        distance_travelled = request.form["c"]
        fuel_price = request.form["d"]
        car_make = request.form["e"]
        average_per_litre = request.form["f"]
        print("Check")
        car = Car(total_budget=total_budget,
                  monthly_budget=monthly_budget,
                  distance_travelled=distance_travelled,
                  fuel_price=fuel_price,
                  car_make=car_make,
                  average_per_litre=average_per_litre)

        db.session.add(car)
        db.session.commit()
    return render_template("test.html")




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/postad", methods=["GET","POST"])
def postad():
    if request.method == "POST":
        if request.files:
            if 'image' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files["image"]
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_name=filename
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = UPLOAD_FOLDER + '/' + filename
                print(filename)
                # return redirect(url_for('uploaded_file',
                #                         filename=filename))
                # # print(file.filename)
                details = run(filename)

                @after_this_request
                def remove_file(response):
                    try:
                        os.remove(filename)
                    except Exception as error:
                        app.logger.error("Error removing or closing downloaded file handle", error)
                    return response

                return render_template("post-ad.html", found=True, filename=image_name, car=details[0], company=details[1], color=details[2])
        else:
            return render_template("post-ad.html")
    else:
        return render_template("post-ad.html")


@app.route("/smartBuy", methods=["GET", "POST"])
def smartBuy():

    if(request.method == "POST"):
        totalBudget = request.form["totalBudget"]
        monthlybudget = request.form["monthlyBudget"]
        travel = request.form["travel"]
        fuel = request.form["fuel"]
        car = Car.query.filter(Car.total_budget <= totalBudget, Car.monthly_budget <= monthlybudget,
                               Car.fuel_price <= fuel, Car.distance_travelled <= travel).first()
        if car:
            print (car.car_make)
            return render_template("buySmart.html", search=True, found=True, car=car.car_make)
    return render_template("buySmart.html", search=False)


if __name__ == '__main__':
    app.run()
