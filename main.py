from Market import app

def DATABASE_INIT():
    from Market import db, models
    with app.app_context():
        db.drop_all()
        db.create_all()
        [db.session.add(models.Item(**item)) for item in [
            {'name': 'IPhone 15', 'barcode': '138729963', 'price': 3000, 'quantity': 2, 'description': '1st item desc'},
            {'name': 'MacBook Air', 'barcode': '154843846', 'price': 8500, 'quantity': 0, 'description': '2nd item desc'},
            {'name': 'Galaxy Z Fold', 'barcode': '854615165', 'price': 10500, 'quantity': 1, 'description': '3rd item desc'},
            {'name': 'Apple iPad', 'barcode': '464147416', 'price': 1500, 'quantity': 3, 'description': '4th item desc'},
            {'name': 'AirPods', 'barcode': '546541689', 'price': 600, 'quantity': 4, 'description': '5th item desc'},
            {'name': 'Smart Watch', 'barcode': '695235148', 'price': 850, 'quantity': 1, 'description': '6th item desc'}
        ]]
        db.session.commit()

if __name__ == "__main__":
    # DATABASE_INIT() # Re-Iniate Database
    app.run(debug=True)
