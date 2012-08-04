from crrr import app


class TestAdmin:

    @classmethod
    def setup_class(self):
        self.app = app.test_client()

    def test_show_volunteer_form(self):
        rv = self.app.get('/volunteer')
        # Verify the form appears
        assert "CRRR Volunteer Application" in rv.data
