from crrr import app


class TestAbout:

    @classmethod
    def setup_class(self):
        self.app = app.test_client()

    def test_show_about(self):
        """The about page should info about the breed."""
        rv = self.app.get('/about')
        assert "References:" in rv.data
