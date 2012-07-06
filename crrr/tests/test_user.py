from crrr.user import User


class TestUser:

    def test_save(self):
        user = User()
        assert user.save()
