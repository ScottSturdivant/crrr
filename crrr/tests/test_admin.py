from crrr import app


class TestAdmin:

    @classmethod
    def setup_class(self):
        self.app = app.test_client()

    def test_show_login(self):
        """Verifies that if /admin is visited without credentials, that a login page is shown."""
        rv = self.app.get('/admin')
        assert "Username" in rv.data
        assert "Password" in rv.data
