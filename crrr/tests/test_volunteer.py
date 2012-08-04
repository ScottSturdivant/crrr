from crrr import app, mail
from crrr.forms import Volunteer


class TestAdmin:

    @classmethod
    def setup_class(self):
        self.app = app.test_client()
        self.fname = "Scott"
        self.lname = "Sturdivant"
        self.email = "asdf@asdf.com"
        self.form = Volunteer(first_name=self.fname,
                              last_name=self.lname,
                              addr_1="8885 S Field Ct",
                              city="Littleton",
                              state="CO",
                              zip_code="80128",
                              email=self.email)

    def test_show_volunteer_form(self):
        """The volunteer page should present a form."""
        rv = self.app.get('/volunteer')
        # Verify the form appears
        assert "CRRR Volunteer Application" in rv.data

    def test_submit_form_sends_mail(self):
        """When submitting the volunteer form, an email should be sent."""
        with mail.record_messages() as outbox:
            rv = self.app.post('/volunteer', data=self.form.data)
        assert len(outbox) == 1

    def test_submit_form_mail_subject(self):
        """When submitting the volunteer form, the email should have a certain subject."""
        with mail.record_messages() as outbox:
            rv = self.app.post('/volunteer', data=self.form.data)
        assert "Volunteer Application Submittal" in outbox[0].subject

    def test_submit_form_mail_sender(self):
        """The sender of the email should be the person submitting the form."""
        with mail.record_messages() as outbox:
            rv = self.app.post('/volunteer', data=self.form.data)
        assert outbox[0].sender == "%s %s <%s>" % (self.fname, self.lname, self.email)

    def test_submit_form_mail_len_recipients(self):
        """The emailed form should go to the person submitting and CRRR."""
        with mail.record_messages() as outbox:
            rv = self.app.post('/volunteer', data=self.form.data)
        assert len(outbox[0].recipients) == 2

    def test_submit_form_mail_recipients_crrr(self):
        """Tests that CRRR gets the form submitted."""
        with mail.record_messages() as outbox:
            rv = self.app.post('/volunteer', data=self.form.data)
        assert 'adoptions@coloradorhodesianridgebackrescue.org' in outbox[0].recipients

    def test_submit_form_mail_recipients_self(self):
        """Tests that the user submitting the form is emailed the results."""
        with mail.record_messages() as outbox:
            rv = self.app.post('/volunteer', data=self.form.data)
        assert '%s %s <%s>' % (self.fname, self.lname, self.email) in outbox[0].recipients

    def test_submit_form_success(self):
        """Tests that the user sees that their form was submitted successfully."""
        with mail.record_messages() as outbox:
            rv = self.app.post('/volunteer', data=self.form.data)
        assert 'Thank you for your interest in becoming a volunteer.' in rv.data
