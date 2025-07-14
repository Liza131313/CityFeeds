from ext import app, db
from models import User

with app.app_context():

    db.drop_all()
    db.create_all()

    admin = User(username="admin", email="admin@gmail.com", password="admin123", role="Admin")

    db.session.add(admin)
    db.session.commit()