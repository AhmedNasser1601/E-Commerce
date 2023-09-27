from Market import app, db
from Market.models import Item, User
from Market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def HomePage():
    return render_template('HOME.html')

@app.route("/market", methods=['GET', 'POST'])
@login_required
def MarketPage():
    if request.method == "POST":
        item_obj = Item.query.filter_by(name=request.form.get('purchased_item')).first()
        if item_obj:
            if current_user.can_purchase(item_obj):
                item_obj.buy(current_user)
                flash(f"Congratulations! You purchased {item_obj.name} for {item_obj.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {item_obj.name}!", category='danger')

        item_obj = Item.query.filter_by(name=request.form.get('sold_item')).first()
        if item_obj:
            if current_user.can_sell(item_obj):
                item_obj.sell(current_user)
                flash(f"Congratulations! You sold {item_obj.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {item_obj.name}!", category='danger')

        return redirect(url_for('MarketPage'))
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('MARKET.html', title='Market', items=items, owned_items=owned_items, purchase_form=PurchaseItemForm(), sell_form=SellItemForm())

@app.route("/register", methods=['GET', 'POST'])
def RegisterPage():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        flash(f'Account created successfully! You are now logged in as: {create_user.username}', category='success')
        return redirect(url_for('MarketPage'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error with creating a user: {error}', category='danger')
    return render_template('REGISTER.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def LoginPage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.password_check(password_attempt=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            if attempted_user.username == 'admin':
                return redirect(url_for('AdminPage'))
            return redirect(url_for('MarketPage'))
        flash('Username and password are not match! Please try again', category='danger')
    return render_template('LOGIN.html', title='Login', form=form)

@app.route("/admin")
@login_required
def AdminPage():
    if not current_user.username=='admin':
        flash('Please login as admin to access the admin panel!', category='danger')
        return redirect(url_for('LoginPage'))
    return render_template('ADMIN.html', title='Admin', users=User.query.all(), items=Item.query.all())

@app.route("/logout")
def LogoutPage():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('HomePage'))
