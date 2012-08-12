from crrr import forms, app


class TestVolunteerForm:

    def test_valid_zip(self):
        with app.test_request_context():
            form = forms.Volunteer(zip_code='80128')
        form.validate()
        assert form.errors.get('zip_code', None) is None

    def test_invalid_zip(self):
        with app.test_request_context():
            form = forms.Volunteer(zip_code='ASDF')
        form.validate()
        assert form.errors.get('zip_code', None) is not None

    def test_valid_first_name(self):
        with app.test_request_context():
            form = forms.Volunteer(first_name='Scott')
        form.validate()
        assert form.errors.get('first_name', None) is None

    def test_invalid_first_name(self):
        with app.test_request_context():
            form = forms.Volunteer(first_name='')
        form.validate()
        assert form.errors.get('first_name', None) is not None

    def test_valid_last_name(self):
        with app.test_request_context():
            form = forms.Volunteer(last_name='Sturdivant')
        form.validate()
        assert form.errors.get('last_name', None) is None

    def test_valid_addr_1(self):
        with app.test_request_context():
            form = forms.Volunteer(addr_1='8885 S. Field Ct')
        form.validate()
        assert form.errors.get('addr_1', None) is None

    def test_valid_addr_2(self):
        with app.test_request_context():
            form = forms.Volunteer(addr_2='8885 S. Field Ct')
        form.validate()
        assert form.errors.get('addr_2', None) is None

    def test_no_addr_2(self):
        with app.test_request_context():
            form = forms.Volunteer(addr_2='')
        form.validate()
        assert form.errors.get('addr_2', None) is None

    def test_valid_city(self):
        with app.test_request_context():
            form = forms.Volunteer(city='Littleton')
        form.validate()
        assert form.errors.get('city', None) is None

    def test_invalid_city(self):
        with app.test_request_context():
            form = forms.Volunteer(city='asdf'*80)
        form.validate()
        assert form.errors.get('city', None) is not None

    def test_no_city(self):
        with app.test_request_context():
            form = forms.Volunteer(city='')
        form.validate()
        assert form.errors.get('city', None) is not None

    def test_valid_email(self):
        with app.test_request_context():
            form = forms.Volunteer(email='scott.sturdivant@gmail.com')
        form.validate()
        assert form.errors.get('email', None) is None
        with app.test_request_context():
            form = forms.Volunteer(email='scott.sturdivant+crrr@gmail.com')
        form.validate()
        assert form.errors.get('email', None) is None
        with app.test_request_context():
            form = forms.Volunteer(email='scott@binrock.net')
        form.validate()
        assert form.errors.get('email', None) is None

    def test_invalid_email(self):
        with app.test_request_context():
            form = forms.Volunteer(email='asdfasdf')
        form.validate()
        assert form.errors.get('email', None) is not None

    def test_no_email(self):
        with app.test_request_context():
            form = forms.Volunteer(email='')
        form.validate()
        assert form.errors.get('email', None) is not None

    def test_valid_phone(self):
        with app.test_request_context():
            form = forms.Volunteer(phone='585-727-1194')
        form.validate()
        assert form.errors.get('phone', None) is None
        with app.test_request_context():
            form = forms.Volunteer(phone='5857271194')
        form.validate()
        assert form.errors.get('phone', None) is None
        with app.test_request_context():
            form = forms.Volunteer(phone='(585) 727-1194')
        form.validate()
        assert form.errors.get('phone', None) is None
        with app.test_request_context():
            form = forms.Volunteer(phone='(585)-727-1194')
        form.validate()
        assert form.errors.get('phone', None) is None

    def test_no_phone(self):
        with app.test_request_context():
            form = forms.Volunteer(phone='')
        form.validate()
        assert form.errors.get('phone', None) is None

    def test_invalid_phone(self):
        with app.test_request_context():
            form = forms.Volunteer(phone_h='(123) 456-78901')
        form.validate()
        assert form.errors.get('phone_h', None) is not None

    def test_valid_state(self):
        with app.test_request_context():
            form = forms.Volunteer(state='CO')
        form.validate()
        assert form.errors.get('state', None) is None

    def test_invalid_state(self):
        with app.test_request_context():
            form = forms.Volunteer(state='AA')
        form.validate()
        assert form.errors.get('state', None) is not None
        with app.test_request_context():
            form = forms.Volunteer(state='')
        form.validate()
        assert form.errors.get('state', None) is not None


class TestLogin:
    def test_username(self):
        with app.test_request_context():
            form = forms.Login(username='admin')
        form.validate()
        assert form.errors.get('username', None) is None

    def test_invalid_username(self):
        with app.test_request_context():
            form = forms.Login(username='a'*80)
        form.validate()
        assert form.errors.get('username', None) is not None

    def test_password(self):
        with app.test_request_context():
            form = forms.Login(password='footron')
        form.validate()
        assert form.errors.get('password', None) is None

    def test_invalid_password(self):
        with app.test_request_context():
            form = forms.Login(password='')
        form.validate()
        assert form.errors.get('password', None) is not None

class TestApplication:
    def test_valid_first_name(self):
        with app.test_request_context():
            form = forms.Application(first_name='Scott')
        form.validate()
        assert form.errors.get('first_name', None) is None

    def test_invalid_first_name(self):
        with app.test_request_context():
            form = forms.Application(first_name='')
        form.validate()
        assert form.errors.get('first_name', None) is not None

    def test_valid_last_name(self):
        with app.test_request_context():
            form = forms.Application(last_name='Scott')
        form.validate()
        assert form.errors.get('last_name', None) is None

    def test_invalid_last_name(self):
        with app.test_request_context():
            form = forms.Application(last_name='')
        form.validate()
        assert form.errors.get('last_name', None) is not None

    def test_valid_addr_1(self):
        with app.test_request_context():
            form = forms.Application(addr_1='8885 S. Field Ct')
        form.validate()
        assert form.errors.get('addr_1', None) is None

    def test_invalid_addr_1(self):
        with app.test_request_context():
            form = forms.Application(addr_1='')
        form.validate()
        assert form.errors.get('addr_1', None) is not None

    def test_valid_addr_2(self):
        with app.test_request_context():
            form = forms.Application(addr_2='8885 S. Field Ct')
        form.validate()
        assert form.errors.get('addr_2', None) is None

    def test_no_addr_2(self):
        with app.test_request_context():
            form = forms.Application(addr_2='')
        form.validate()
        assert form.errors.get('addr_2', None) is None

    def test_valid_city(self):
        with app.test_request_context():
            form = forms.Application(city='Littleton')
        form.validate()
        assert form.errors.get('city', None) is None

    def test_invalid_city(self):
        with app.test_request_context():
            form = forms.Application(city='')
        form.validate()
        assert form.errors.get('city', None) is not None

    def test_no_city(self):
        with app.test_request_context():
            form = forms.Application(city='')
        form.validate()
        assert form.errors.get('city', None) is not None

    def test_valid_email(self):
        with app.test_request_context():
            form = forms.Application(email='scott.sturdivant@gmail.com')
        form.validate()
        assert form.errors.get('email', None) is None
        with app.test_request_context():
            form = forms.Application(email='scott.sturdivant+crrr@gmail.com')
        form.validate()
        assert form.errors.get('email', None) is None
        with app.test_request_context():
            form = forms.Application(email='scott@binrock.net')
        form.validate()
        assert form.errors.get('email', None) is None

    def test_invalid_email(self):
        with app.test_request_context():
            form = forms.Application(email='asdfasdf')
        form.validate()
        assert form.errors.get('email', None) is not None

    def test_no_email(self):
        with app.test_request_context():
            form = forms.Application(email='')
        form.validate()
        assert form.errors.get('email', None) is not None
