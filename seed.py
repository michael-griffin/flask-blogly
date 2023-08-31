from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post


db.drop_all()
db.create_all()

michael = User(first_name='Michael', last_name='Griffin', image_url=DEFAULT_IMAGE_URL)
josh = User(first_name='Joshua', last_name='Hellstrom')

db.session.add(michael)
db.session.add(josh)

db.session.commit()