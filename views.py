#The views are storerd and programmed here except for the login that goes into auth (authentication)
from flask import Blueprint, render_template
from flask_login import  login_required, current_user
from .models import Animal, Activity, User
from . import db

#This file is a blueprint of our application to organize our views

views = Blueprint('views', __name__)


#This stores the path for the root main as it has just the slash
@views.route('/')
#this function will run whenever we go to that path
def home():
    from werkzeug.security import generate_password_hash
    mod = User.query.filter_by(first_name="moderador").first()
    if not mod:
        pas = "moderador"
        haspass = generate_password_hash(pas, method='sha256')
        db.session.add(User(email="moderador@gmail.com", password = haspass, first_name = "Moderador", role = 1))
        db.session.commit()

    act1 = Activity.query.filter_by(name="Dormir con delfines").first()
    if not act1:
        toadd =[] 
        a = Activity(name = "Dormir con delfines", location = "Acuario", price = 25.6, date = "2022-12-23 22:00:00.0", aforo = 20, featured=1)
        toadd.append(a)
        b = Activity(name = "Alimentar Leones", location = "Hábitat sabana", price = 100, date = "2023-01-23 14:30:00.0", aforo = 10, featured=1)
        toadd.append(b)
        c = Activity(name = "Comer guayabas con los monos", location = "Hábitat Jungla", price = 5, date = "2022-11-23 22:00:00.0", aforo = 0, featured=0)
        toadd.append(c)
        d = Activity(name = "Alimentar focas", location = "Tierra de Hielo", price = 25.6, date = "2022-12-23 12:00:00.0", aforo = 20, featured=0)
        toadd.append(d)
        e = Activity(name = "Celebra tu cumple", location = "Catacumbas", price = 50, date = "2023-11-26 16:15:00.0", aforo = 25, featured=1)
        toadd.append(e)
        f = Activity(name = "Pelea a muerte contra gorilas", location = "Ring de boxeo", price = 200, date = "2022-12-23 22:00:00.0", aforo = 20, featured=0)
        toadd.append(f)
        g = Activity(name = "Dormir con delfines", location = "Auario", price = 25.6, date = "2022-12-21 22:00:00.0", aforo = 20, featured=0)
        toadd.append(g)
        db.session.add_all(toadd)
        db.session.commit()
    f_activities = Activity.query.filter_by(featured = 1).all()
    return render_template("home.html", user=current_user, activity = f_activities)

@views.route('/animal_catalog')
def animal_catalog():
    cond = Animal.query.filter_by(id=1).first()
    if not cond:
        toadd =[] 
        a = Animal(name="Carpincho", sci_name = "Hydrochoerus hydrochaeris", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(a)
        b = Animal(name="Charrancito Americano", sci_name = "Sternula antillarum", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(b)
        c = Animal(name="Foca", sci_name = "Phoca Virtulina", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(c)
        d = Animal(name="Lagarto", sci_name = "Varanus Panoptes", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(d)
        e = Animal(name="Lémur", sci_name = "Lemur Catta", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(e)
        f = Animal(name="León Marino", sci_name = "Otariinae", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(f)
        g = Animal(name="Lirón", sci_name = "gliridae", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(g)
        h = Animal(name="Quokka", sci_name = "Setonix", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(h)
        i = Animal(name="Estornino", sci_name = "Spreo bicolor", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(i)
        j = Animal(name="Tiburón Martillo", sci_name = "sphyrna mokarran", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(j)
        k = Animal(name="Tucán", sci_name = "Ramphastos tukanum", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(k)
        l = Animal(name="Boa del desierto Árabe", sci_name = "Eryx johnii", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(l)
        m = Animal(name="Pez Luna", sci_name = "Mola Mola", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(m)
        n = Animal(name="Ardilla Andaluza", sci_name = "Sternula antillarum", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(n)
        o = Animal(name="Zorro Ártico", sci_name = "Sternula antillarum", info = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...")
        toadd.append(o)
        db.session.add_all(toadd)
        db.session.commit()
    animal=Animal.query.order_by(Animal.name).all()
    return render_template("animal_catalog.html", user=current_user, animal = animal)

@views.route("/animal/<int:animal_id>")
def animal(animal_id):
    animal=Animal.query.filter_by(id=animal_id).first_or_404()
    return render_template("animal.html", user=current_user, animal=animal)

@views.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html", user = current_user)

