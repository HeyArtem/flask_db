from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


"""
Простеший скрипт Flask & db 
html-форма ввода и вывод

$ pip install Flask
$ pip install Flask-SQLAlchemy
$ pip install -U flask_migrate
"""

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shampoo.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Shampoo(db.Model):
    __tablename__ = "Shampoo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(120))
    price = db.Column(db.String(20))
    created = db.Column(db.String(30))

    # def __init__(self, name, description, price):
    #     self.name = name
    #     self.description = description
    #     self.price = price  

    def __repr__(self):
        return f"name: {self.name} \ndescription: {self.description}"
    

# Это прописываю в консоли:
# $ python
# from app import app, db
# app.app_context().push()
# db.create_all()
# ctr + D выход


# Главная, выводит данные db
@app.route("/")
def index():
    info = Shampoo.query.all()

    return render_template("shampoo.html", list=info)


@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        created = request.form["created"]

        # Автоматичесское присваивание Даты
        now = datetime.now()

        # Условие: если пользователь при вводе, прописал дату, то в БД запишется эта дата
        if request.form["created"]:
            created = request.form["created"]
        
        # Если пользователь не присвоил дату, то в БД запишется текущая дата
        else:
            created = now.strftime("%d-%m-%Y")

        info = Shampoo(name=name, description=description, price=price, created=created)

        # Пробую записать в БД
        try:
            db.session.add(info)
            db.session.commit()

            # После записи в БД перенаправляю пользователя на главную страницу
            return redirect("/")
        
        except:
            return "Ошибка ввода данных"
    
    # Если метод "GET" открываю пользователю страницу ввода данных
    else:
        return render_template("create.html")


    


if __name__ == "__main__":
    app.run(debug=True)
