from Market import app, db
from Market.models import Item, User
from Market.forms import RegisterForm, LoginForm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

@app.route("/")
def HomePage():
    return render_template('HOME.html')

@app.route("/about")
def AboutPage():
    return render_template('ABOUT.html', title='About')

@app.route("/products")
def ProductsPage():
    if not current_user.is_authenticated:
        flash('Please login to access the products page!', category='danger')
        return redirect(url_for('LoginPage'))
    return render_template('PRODUCTS.html', title='Products', items=Item.query.all())

@app.route("/sellers")
def SellersPage():
    if not current_user.is_authenticated:
        flash('Please login to access the sellers page!', category='danger')
        return redirect(url_for('LoginPage'))
    return render_template('SELLERS.html', title='Sellers', users=User.query.all())

@app.route("/register", methods=['GET', 'POST'])
def RegisterPage():
    if current_user.is_authenticated:
        return redirect(url_for('HomePage'))
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data
        )
        db.session.add(create_user)
        db.session.commit()
        return redirect(url_for('ProductsPage'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error with creating a user: {error}', category='danger')
    return render_template('REGISTER.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def LoginPage():
    if current_user.is_authenticated:
        return redirect(url_for('HomePage'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.password_check(password_attempt=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            if attempted_user.username == 'admin':
                return redirect(url_for('AdminPage'))
            return redirect(url_for('ProductsPage'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('LOGIN.html', title='Login', form=form)

@app.route("/admin")
def AdminPage():
    if not current_user.is_authenticated or current_user.username!='admin':
        flash('Please login as admin to access the admin panel!', category='danger')
        return redirect(url_for('LoginPage'))
    return render_template('ADMIN.html', title='Admin', users=User.query.all(), items=Item.query.all())

@app.route("/logout")
def LogoutPage():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out!', category='info')
    return redirect(url_for('HomePage'))
