#!/usr/bin/env python
"""
This script is intended to take data from csv files dumped from the original
mysql database and add them to the dev or production databases.
"""
import argparse
from crrr import db
from crrr.models import (
        Dog,
        User,
        Address,
        )

def str_to_bool(foo):
    return True if foo.lower() in ['y', 'yes', 'true', '1'] else False

def import_dogs(dog_csv):
    """
    Dump the dogs info with this cmd:
    mysql -u crrrescue -ppass crrrescue -B -e "SELECT * FROM Dog_info;" | sed '1d;s/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > dog.csv
    """
    print "Processing ", dog_csv
    with open(dog_csv) as f:
        for i, line in enumerate(f):
            row = line.split('","')
            id, name, status, breed, sex, age, mix, size, fee, desc, special, nodogs, nocats, nokids, fixed, shots, house, url1, url2, url3, archive, tails = row 

            dog = Dog()
            dog.id = int(id.strip('"'))
            dog.name = name
            dog.status = status.lower()
            dog.breed = breed
            dog.sex = sex
            dog.age = age.lower()
            dog.mix = str_to_bool(mix)
            dog.size = size.lower()
            dog.fee = int(fee.partition('.')[0].strip('$')) if fee else 0
            dog.description = desc.replace('\x93', '"').replace('\x94', '"').replace('\x92', "'").replace('\x96', '-')
            dog.special_needs = str_to_bool(special)
            dog.home_without_dogs = str_to_bool(nodogs)
            dog.home_without_cats = str_to_bool(nocats)
            dog.home_without_kids = str_to_bool(nokids)
            dog.fixed = str_to_bool(fixed)
            dog.shots = str_to_bool(shots)
            dog.housetrained = str_to_bool(house)
            dog.archive = str_to_bool(archive)
            dog.happy_tails = tails.strip()

            print "Created: ", dog

            db.session.add(dog)
        db.session.commit()
        print "Addded %d dogs." % (i + 1)

def import_users(user_csv):
    """
    Dump the users info with this cmd:
    mysql -u crrrescue -ppass crrrescue -B -e "SELECT * FROM auth;" | sed '1d;s/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > users.csv
    """
    print "Processing ", user_csv
    with open(user_csv) as f:
        for i, line in enumerate(f):
            uname, password, fname, lname, addr = line.split('","')

            user = User()
            user.username  = uname.strip('"')
            user.password  = password
            user.firstname = fname
            user.lastname  = lname
            user.role = 1
            user.id = i

            # If there was an address associated with a user, add it too
            addr = addr.replace('"', '').strip()
            if addr:
                address = Address()
                address.user_id = user.id
                address.state = 'CO'
                address.location = 'home'
                if 'Littleton' in addr:
                    address.line_1 = addr.split('Littleton')[0].strip()
                    address.city = 'Littleton'
                    address.zip = addr.split(' ')[-1]
                elif 'Lakewood' in addr:
                    address.line_1 = addr.split('Lakewood')[0].strip()
                    address.city = 'Lakewood'
                    address.zip = addr.split(' ')[-1]
                print "Created address: ", address

            user.addresses.append(address)

            print "Created: ", user

            db.session.add(user)
        db.session.commit()
        print "Added %d users." % (i + 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recreate',
                        help='Drop and re-create all tables.',
                        action='store_true')
    parser.add_argument('--dog-csv',
                        help='The csv file containing the Dog_info table.')
    parser.add_argument('--user-csv',
                        help='The csv file containing the auth table.')
    args = parser.parse_args()

    if args.recreate:
        print "Dropping all tables."
        db.drop_all()
        print "Creating all tables."
        db.create_all()
    if args.dog_csv:
        import_dogs(args.dog_csv)
    if args.user_csv:
        import_users(args.user_csv)


if __name__ == '__main__':
    main()
