import os

os.environ["DATABASE_URL"] = "postgresql:///users_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        db.drop_all()
        db.create_all()

        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title="test1_title",
            content="test1_content",
            user_id = test_user.id,
        )

        db.session.add(test_post)
        db.session.commit()

        self.user_id = test_user.id
        self.post_id = test_post.id

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.



    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    #@app.get('/')
    def test_list_redirect(self):
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 302)

    #@app.get('/users')
    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    #@app.get('/users/new')
    def test_new_users_get(self):
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<h1> Create a User ", html)

    #@app.post('/users/new')
    def test_new_users_post(self):
        with self.client as c:
            new_user_form = {
                "first_name": "John",
                "last_name": "Smith",
                "image_url": "default-image.jpg"
            }

            resp = c.post('/users/new', data=new_user_form, follow_redirects=True)

            user = User.query.filter_by(first_name = 'John').one_or_none()

            self.assertEqual(user.first_name == 'John', True)
            self.assertIsInstance(user, User)

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("John", html)
            self.assertIn("Smith", html)





    # Test for users/posts page that contains the right info
    def test_individual_user_and_posts(self):
        """Check if our individual user page is showing post title"""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            print("HTML", html)

            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)
            self.assertIn("test1_title", html)


    #Check individual post
    def test_individual_posts(self):
        """check post detail page has title + content of automade post"""
        with self.client as c:
            print(f"/posts/{self.post_id}")

            # print(f"Idea 2: {c.post_id}")
            resp = c.get(f"/posts/{self.post_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("test1_title", html)
            self.assertIn("test1_content", html)


    #Check edit posts
    def test_edit_post_page(self):
        """Check if auto made post autofills on edit post page"""
        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Post", html)
            self.assertIn("test1_title", html)
            self.assertIn("test1_content", html)


    def test_edit_post_post(self):
        """makes a new test post, add it to table, then check its presence in table"""
        with self.client as c:
            new_post_form = {
                "title": "new_title",
                "content": "new_content"
            }
            resp = c.post(f"/posts/{self.post_id}/edit", data=new_post_form)
            self.assertEqual(resp.status_code, 302)

            post = Post.query.filter_by(title = "new_title").one()
            self.assertIsInstance(post, Post)
            self.assertEqual(post.title == 'new_title', True)


    #Test delete post
    def test_delete_post(self):
        """Tests that post is removed from table, and redirect happens"""
        with self.client as c:

            resp = c.post(f"posts/{self.post_id}/delete")
            self.assertEqual(resp.status_code, 302)
            post = Post.query.filter_by(title = "new_title").one_or_none()
            self.assertEqual(post, None)

