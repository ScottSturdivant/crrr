import os
import crrr
import tempfile

class TestCrrr:

    def setup_method(self, method):
        self.db_fd, self.tmpdb = tempfile.mkstemp()
        crrr.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % self.tmpdb
        crrr.app.config['TESTING'] = True
        crrr.app.config['CSRF_ENABLED'] = False
        self.app = crrr.app.test_client()
        crrr.db.create_all()

    def teardown_method(self, method):
        os.close(self.db_fd)
        os.unlink(self.tmpdb)

    def add_user(self, username, email, password, admin):
        user = crrr.models.User(username, email, password, admin)
        crrr.db.session.add(user)
        crrr.db.session.commit()

    def add_dog(self, name='Rodeo', adopted=True, breed='Ridgeback', sex='M',
                age='Adult', mix=False, size='L', fee=85, description='Big and lazy.',
                special_needs=False, home_without_dogs=False, home_without_cats=True,
                home_without_kids=False, spayed=True, shots=True, housetrained=True,
                photo1_url=None, photo2_url=None, photo3_url=None, archive=False,
                happy_tails='A nice life.'):
        dog = crrr.models.Dog(name=name, adopted=adopted, breed=breed, sex=sex, age=age, mix=mix,
                              size=size, fee=fee, description=description, special_needs=special_needs,
                              home_without_dogs=home_without_dogs, home_without_cats=home_without_cats,
                              home_without_kids=home_without_kids, spayed=spayed, shots=shots,
                              housetrained=housetrained, photo1_url=photo1_url, photo2_url=photo2_url,
                              photo3_url=photo3_url, archive=archive, happy_tails=happy_tails)
        crrr.db.session.add(dog)
        crrr.db.session.commit()

    def login(self, username, password):
        with crrr.app.test_request_context():
            form = crrr.forms.Login(username=username, password=password)
        return self.app.post('/login?next=/admin', data=form.data, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        """Tests that a user accessing the admin page is redirected to login."""
        username = 'admin'
        password = 'pass'
        self.add_user(username, 'foo@foo.com', password, True)
        rv = self.app.get('/admin', follow_redirects=True)
        assert 'Username' in rv.data
        assert 'Password' in rv.data
        rv = self.login(username, password)
        assert "Welcome" in rv.data

    def test_available_dogs(self):
        """Shows that adoptable dogs appear once added."""
        rv = self.app.get('/available_dogs')
        assert 'no dogs available' in rv.data
        self.add_dog(name='Rodeo', adopted=False)
        self.add_dog(name='Mackenzie', adopted=False)
        self.add_dog(name='Nala', adopted=True)
        rv = self.app.get('/available_dogs')
        assert 'Rodeo' in rv.data
        assert 'Mackenzie' in rv.data
        assert 'Nala' not in rv.data


