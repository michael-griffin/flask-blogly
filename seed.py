from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post, Tag, PostTag


db.drop_all()
db.create_all()

# For testing database initially
michael = User(first_name='Michael', last_name='Griffin', image_url=DEFAULT_IMAGE_URL)
josh = User(first_name='Joshua', last_name='Hellstrom')

db.session.add(michael)
db.session.add(josh)
db.session.commit()


test_post = Post(
    title="user1 title",
    content="user1 content",
    user_id = michael.id,
)

test_post_2 = Post(
    title="user2 title",
    content="user2 content",
    user_id = josh.id,
)


tag1 = Tag(name="tag1")
tag2 = Tag(name="tag2")

post_tag1 = PostTag(post_id=1, tag_id=1)
# post_tag2 = PostTag(post_id=test_post_2.id, tag_id=tag2.id)

db.session.add(test_post)
db.session.add(test_post_2)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(post_tag1)
# db.session.add(post_tag2)


db.session.commit()



