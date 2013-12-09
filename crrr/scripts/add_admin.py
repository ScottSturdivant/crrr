#!/usr/bin/env python
"""
Creates administrative users
"""
import argparse
import os
import getpass
from crrr import db
from crrr.admin.models import (
        User,
        Address,
from crrr.admin.models.user import ROLE_ADMIN
CODEC = 'utf-8'

def add_user(username, firstname, lastname):
    print "Processing ", username
    user = User()
    user.username  = username
    user.set_password(getpass.getpass().strip())
    user.firstname = firstname
    user.lastname = lastname
    user.role = ROLE_ADMIN

    print "Created: ", user

    db.session.add(user)
    db.session.commit()
    print "Added user."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username',
                        help='The username of the admin user.')
    parser.add_argument('--firstname',
                        help='The users first name.')
    parser.add_argument('--lastname',
                        help='The users last name.')
    args = parser.parse_args()

    add_user(args.username, args.firstname, args.lastname)

if __name__ == '__main__':
    main()
