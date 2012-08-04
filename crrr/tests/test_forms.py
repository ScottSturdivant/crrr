from crrr import forms


class TestVolunteerForm:

    def test_valid_zip(self):
        form = forms.Volunteer(zip_code='80128')
        form.validate()
        assert form.errors.get('zip_code', None) is None

    def test_invalid_zip(self):
        form = forms.Volunteer(zip_code='ASDF')
        form.validate()
        assert form.errors.get('zip_code', None) is not None

    def test_valid_first_name(self):
        form = forms.Volunteer(first_name='Scott')
        form.validate()
        assert form.errors.get('first_name', None) is None

    def test_invalid_first_name(self):
        form = forms.Volunteer(first_name='')
        form.validate()
        assert form.errors.get('first_name', None) is not None

    def test_valid_last_name(self):
        form = forms.Volunteer(last_name='Sturdivant')
        form.validate()
        assert form.errors.get('last_name', None) is None

    def test_valid_addr_1(self):
        form = forms.Volunteer(addr_1='8885 S. Field Ct')
        form.validate()
        assert form.errors.get('addr_1', None) is None

    def test_valid_addr_2(self):
        form = forms.Volunteer(addr_2='8885 S. Field Ct')
        form.validate()
        assert form.errors.get('addr_2', None) is None

    def test_no_addr_2(self):
        form = forms.Volunteer(addr_2='')
        form.validate()
        assert form.errors.get('addr_2', None) is None

    def test_valid_city(self):
        form = forms.Volunteer(city='Littleton')
        form.validate()
        assert form.errors.get('city', None) is None

    def test_invalid_city(self):
        form = forms.Volunteer(city='asdf'*80)
        form.validate()
        assert form.errors.get('city', None) is not None

    def test_no_city(self):
        form = forms.Volunteer(city='')
        form.validate()
        assert form.errors.get('city', None) is not None

    def test_valid_email(self):
        form = forms.Volunteer(email='scott.sturdivant@gmail.com')
        form.validate()
        assert form.errors.get('email', None) is None
        form = forms.Volunteer(email='scott.sturdivant+crrr@gmail.com')
        form.validate()
        assert form.errors.get('email', None) is None
        form = forms.Volunteer(email='scott@binrock.net')
        form.validate()
        assert form.errors.get('email', None) is None

    def test_invalid_email(self):
        form = forms.Volunteer(email='asdfasdf')
        form.validate()
        assert form.errors.get('email', None) is not None

    def test_no_email(self):
        form = forms.Volunteer(email='')
        form.validate()
        assert form.errors.get('email', None) is not None

    def test_valid_phone(self):
        form = forms.Volunteer(phone='585-727-1194')
        form.validate()
        assert form.errors.get('phone', None) is None
        form = forms.Volunteer(phone='5857271194')
        form.validate()
        assert form.errors.get('phone', None) is None
        form = forms.Volunteer(phone='(585) 727-1194')
        form.validate()
        assert form.errors.get('phone', None) is None
        form = forms.Volunteer(phone='(585)-727-1194')
        form.validate()
        assert form.errors.get('phone', None) is None

    def test_no_phone(self):
        form = forms.Volunteer(phone='')
        form.validate()
        assert form.errors.get('phone', None) is None

    def test_invalid_phone(self):
        form = forms.Volunteer(phone='(123) 456-78901')
        form.validate()
        assert form.errors.get('phone', None) is not None

    def test_valid_state(self):
        form = forms.Volunteer(state='CO')
        form.validate()
        assert form.errors.get('state', None) is None

    def test_invalid_state(self):
        form = forms.Volunteer(state='AA')
        form.validate()
        assert form.errors.get('state', None) is not None
        form = forms.Volunteer(state='')
        form.validate()
        assert form.errors.get('state', None) is not None


class TestLogin:
    def test_username(self):
        form = forms.Login(username='admin')
        form.validate()
        assert form.errors.get('username', None) is None

    def test_invalid_username(self):
        form = forms.Login(username='a'*80)
        form.validate()
        assert form.errors.get('username', None) is not None

    def test_password(self):
        form = forms.Login(password='footron')
        form.validate()
        assert form.errors.get('password', None) is None

    def test_invalid_password(self):
        form = forms.Login(password='')
        form.validate()
        assert form.errors.get('password', None) is not None
