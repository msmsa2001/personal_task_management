from flask import Blueprint,render_template,request,flash,redirect,url_for
auth=Blueprint('auth',__name__)
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('view.home'))
            else:
                flash('incorrect password',category='error')
        else:
            flash('Email does not exits.',category='error')
    return render_template('login.html',boolean=False,user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email=request.form.get('email')
        fname=request.form.get('fname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        user=User.query.filter_by(email = email).first()
        if user:
            flash("Email already exits.",category='error')
        elif len(email) < 4:
            flash("Enter Valid Email id",category='error')
        elif len(fname) < 2:
            flash("Enter Valid Name",category='error')
        elif password1 != password2:
            flash("Password Mismatched",category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 character.",category='error')
        else:
            new_user=User(email=email,first_name=fname,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account Created",category='success')
            return redirect(url_for('view.home'))


    return render_template('sign_up.html',user=current_user)
