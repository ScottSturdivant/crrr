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

