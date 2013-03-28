#!/usr/bin/env python
"""
This script is intended to take data from csv files dumped from the original
mysql database and add them to the dev or production databases.
"""
import csv
import argparse
from crrr import db
from crrr.models import Dog


def import_dogs(dog_csv):
    print "Processing ", dog_csv
    with open(dog_csv, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print row
            id, name, status, breed, sex, age, mix, size, fee, desc, special,
            nodogs, nocats, nokids, fixed, shots, house, url1, url2, url3,
            archive, tails = row 

            dog = Dog()
            dog.id = id
            dog.name = name
            dog.status = status
            dog.breed = breed
            dog.sex = sex
            dog.age = age
            dog.mix = mix
            dog.size = size
            dog.fee = fee
            dog.description = desc
            dog.special_needs = special
            dog.home_without_dogs = nodogs
            dog.home_without_cats = nocats
            dog.home_without_kids = nokids
            dog.fixed = fixed
            dog.shots = shots
            dog.housetrained = house
            dog.archive = archive
            dog.happy_tails = tails

            print "Created: ", dog

            db.session.add(dog)
        db.session.commit()


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
