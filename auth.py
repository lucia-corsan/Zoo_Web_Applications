from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
#to secure passwords
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Activity, Reserve, Animal
from . import db
from flask_login import login_user,LoginManager, login_required, logout_user, current_user
from fpdf import FPDF


#This file is a blueprint of our application (authentication) to organize our views

auth = Blueprint('auth', __name__)

#In this page i want to define login, logout and sign up, setting up their route

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #checking if the user email is valid or not
        #REALLY USEFUL FUNCTION
        user = User.query.filter_by(email=email).first()
        if user:
            #check if the password is the users 
            if check_password_hash(user.password, password):
                flash('Logged in', category = 'success')
                #logs the user and remembers that it is remembered while the server runs
                login_user(user, remember = True)
            else:
                flash('Incorrect password', category='error')
        else:
            flash('The user does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/customer_profile', methods =['GET','POST'])
@login_required
def customer_profile():
    reserve = Reserve.query.filter_by(user_id=int(current_user.id)).all()
    activities =[] 
    for i in reserve:
        act = Activity.query.filter_by(id = int(i.sa_id)).all()
        activities.append(act)

    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        seats = request.form.get('seats')
        price = request.form.get('price')
        date = request.form.get('date')
        featured = request.form.get('options')
       #recastear ft 

        if featured == "yes":
            featured = 1
        else:
            featured = 0

        a = Activity(name = name, location=location, aforo=int(seats), price = int(price), date = date, featured=featured)
        db.session.add(a)
        db.session.commit()
        flash('Activity created!', category='success')
  
       

  
    return render_template("customer_profile.html", user=current_user, reserve = reserve, activities = activities)

@auth.route("/activity")
def activity():

    activity = Activity.query.all()
    return render_template("activity.html", user=current_user, activity = activity)


@auth.route("/edit/<int:activity_id>", methods =['GET', 'POST'])
@login_required
#continuar
def edit(activity_id):
    if request.method == 'POST':
            date = request.form.get('date') 
            featured = request.form.get('options')

            if featured == "yes":
                    featured = 1
            else:
                featured = 0   

            aa = Activity.query.filter_by(id=activity_id).first()
            aa.date = date
            aa.featured = featured
            db.session.commit()

    return render_template("edit.html", user=current_user, activity=activity)

@auth.route("/reserve/<int:activity_id>", methods =['GET', 'POST'])
@login_required
def reserve(activity_id):
    #Selecciono el usuario 
    user=current_user
    #Selecciono la actividad
    activity=Activity.query.filter_by(id=activity_id).first_or_404()
    if activity.aforo ==0:
        flash('We are fully booked!', category='error')
    if request.method == 'POST':
        #Cojo el numero de plazas reservadas del form 
        n_tickets = request.form.get('n_tickets')
        activity.aforo -= int(n_tickets)
        reserve = Reserve(user_id=user.id, sa_id=activity.id, n_tickets=n_tickets)
        db.session.add(reserve)
        db.session.commit()
        flash('Reservation complete!', category='success')


    return render_template("reserve.html", user=user, activity=activity)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    #Con esto checkeo que metodo se ha usado para llegar a la página
    if request.method == 'POST':
        #conseguir cosas del form
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #Test to add the new user to the database  
        c = 0
        for i in range(0, len(password1)):
            if (password1[i]) in ["1","2","3","4","5","6","7","8","9","0"] :
                c = 1
        c2 = 0
        for i in range(0, len(password1)):
            if (password1[i]) in ["!","$","&","€","(",")","=","¿","?","¡"] :
                c2 = 1

        #now lets handle possible errors in the form
        cond = User.query.filter_by(email=email).first()
        if cond:
            flash('There already is an account for this email', category='error')
            return redirect(url_for('views.home'))
        elif len(email) <= 3:
            #Flash helps us to notify the users things that are important
            flash('Email must have 4 characters or more', category= 'error')
            pass
        elif len(first_name) < 1:
            flash('Invalid name, too short', category= 'error')
            pass
        elif password1 != password2:
            flash('Passwords do not coincide', category= 'error')
            pass
        elif c == 0:
            flash('Passwords must be have at least one number', category= 'error')
            pass
        elif c2 == 0:
            flash('Passwords must be have at least one symbol [!/¡/¿/?/$/&/(/)/=/€]', category= 'error')
            pass
        elif len(password1) < 8:
            flash('Passwords must be at least 8 characters', category= 'error')
            pass
        else:#if everything has gone correctly I will create a new user
            new_user = User(email = email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), role = False)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created, Welcome!', category='success')
            login_user(new_user, remember = True)

            return redirect(url_for('views.home'))


    return render_template("signup.html", user=current_user)


@auth.route('/diploma/<int:animal_id>', methods =['GET','POST'])
@login_required

def jpg_to_pdf(animal_id):
    animal=Animal.query.filter_by(id=animal_id).first_or_404()

    pdf = FPDF()
    pdf.add_page()
     
    pdf.set_font("Arial", size = 15) 
    
    pdf.cell(200, 10, txt = "Zoo de Torremocha certifies that",  
            ln = 1, align = 'C') 
    
    pdf.cell(200, 10, txt = animal.name + ", whose species' name is " + animal.sci_name + " was adopted by " + current_user.first_name, 
            ln = 2, align = 'C') 

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename='diploma.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response