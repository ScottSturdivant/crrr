#!/usr/bin/env python
"""
This script is intended to take data from csv files dumped from the original
mysql database and add them to the dev or production databases.
"""
import argparse
from crrr import db
from crrr.models import Dog

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recreate',
                        help='Drop and re-create all tables.',
                        action='store_true')
    parser.add_argument('--dog-csv',
                        help='The csv file containing the Dog_info table.')
    args = parser.parse_args()

    if args.recreate:
        print "Dropping all tables."
        db.drop_all()
        print "Creating all tables."
        db.create_all()
    if args.dog_csv:
        import_dogs(args.dog_csv)


if __name__ == '__main__':
    main()
