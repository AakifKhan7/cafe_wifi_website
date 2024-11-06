from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'aakif_khan5252'
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


@app.route('/')
def home():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form['name'],
            map_url=request.form['map_url'],
            img_url=request.form['img_url'],
            location=request.form['location'],
            seats=request.form['seats'],
            has_toilet='has_toilet' in request.form,
            has_wifi='has_wifi' in request.form,
            has_sockets='has_sockets' in request.form,
            can_take_calls='can_take_calls' in request.form,
            coffee_price=request.form['coffee_price']
        )
        try:
            db.session.add(new_cafe)
            db.session.commit()
            flash("Cafe added successfully!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Cafe with this name already exists.", "error")
        return redirect(url_for('home'))
    return render_template('add_cafe.html')

@app.route('/cafe/<int:cafe_id>')
def cafe_detail(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    return render_template('cafe_detail.html', cafe=cafe)

@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        flash("Cafe deleted successfully!", "success")
    else:
        flash("Cafe not found.", "error")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
