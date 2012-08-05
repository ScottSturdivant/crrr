from crrr import app


class Test404:

    @classmethod
    def setup_class(self):
        self.app = app.test_client()

    def test_invalid_page(self):
        """Try to access a page we didn't define a view for."""
        rv = self.app.get('/foobar')
        assert "Ruh roh" in rv.data
