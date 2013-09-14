#!/usr/bin/env python
"""
This script is intended to take data from csv files dumped from the original
mysql database and add them to the dev or production databases.
"""
import argparse
import os
from crrr import db
from crrr.dogs.models import (
        Dog,
        Picture,
        )
from crrr.user.models import (
        User,
        Address,
        Profile,
        Pet,
        Employment,
        Family,
        Phone
        )
from crrr.root.models import (
        App,
        )
CODEC = 'utf-8'

# The existing database had a few spam entries that we'd like to ignore.
BAD_APPS = [477, 478, 641, 645, 670, 671, 673, 674, 675, 676, 677, 682, 683, 684, 687]

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
            dog.setStatus(status.lower())
            dog.breed = breed
            dog.setSex(sex)
            dog.age = age.lower()
            dog.mix = str_to_bool(mix)
            dog.setSize(size.lower())
            dog.fee = int(fee.partition('.')[0].strip('$')) if fee else 0
            dog.description = unicode(desc.strip(), CODEC, 'ignore')
            dog.special_needs = str_to_bool(special)
            dog.home_without_dogs = str_to_bool(nodogs)
            dog.home_without_cats = str_to_bool(nocats)
            dog.home_without_kids = str_to_bool(nokids)
            dog.fixed = str_to_bool(fixed)
            dog.shots = str_to_bool(shots)
            dog.housetrained = str_to_bool(house)
            dog.archive = str_to_bool(archive)
            dog.happy_tails = tails.strip('"\n') if tails.strip('"\n') else None

            pictures = []
            for url in [url1, url2, url3]:
                if url:
                    pictures.append(Picture(file_url=url, thumb_url="tb_"+url))
            dog.pictures.extend(pictures)

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
            user.set_password(os.environ.get('ADMIN_PASSWORD', password))
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

def import_apps(app_csv):
    """
    Dump the apps info with this cmd:
    mysql -u crrrescue -ppass crrrescue -B -e "SELECT * FROM Apps" | sed '1d;s/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > apps.csv
    """
    print "Processing ", app_csv
    with open(app_csv) as f:
        for i, line in enumerate(f):
            row = line.split('","')
            # There are a few apps that i have no idea how they got there, but
            # we can ignore!
            if int(row[0].strip('"')) in BAD_APPS:
                print "Throwing out app: ", row[0]
                continue

            # Now to co-erce this data into our new format...
            app = App()
            app.id = row[0].strip('"')
            app.date = row[2]
            app.status = row[3].lower()
            app.notes = row[6]
            app.archive = str_to_bool(row[104].strip('"\n'))

            # Users may have submitted multiple applications, meaning that
            # their email address (which is what we now key off to make unique
            # user accounts) may be repeated, which doesn't allow us to create
            # new users for each of those apps.  Therefore we need to see if a
            # user already exists.

            user = db.session.query(User).filter(User.email==row[17]).first()

            if not user:
                user = User(username=row[17], # email
                            email=row[17],
                            first_name=row[7],
                            last_name=row[8],
                            password='changeme',
                            active=False)

            # Get their home and vet addresses.  Note that originally before a
            # vet, I believe it must have been a personal reference, so this
            # data may seem a bit funky.
            home = Address(location='home',
                           line_1=row[9],
                           line_2=row[10] if row[10] else None,
                           city=row[11],
                           state=row[12],
                           zip=row[13],
                           duration=unicode(row[18], CODEC, 'ignore'))
            vet = Address(location='vet',
                          clinic=row[34] if row[34] else None,
                          vet_name=row[35] if row[35] else None,
                          line_1=row[36] if row[36] else None,
                          line_2=row[37] if row[37] else None,
                          city=row[38] if row[38] else None,
                          state=row[39] if row[39] else None,
                          zip=row[40] if row[40] else None)
            phone = Phone(number=row[41], location='work')
            vet.phones.append(phone)
            user.addresses.extend([home, vet])

            # Get the user's phone numbers
            home = Phone(number=row[14] if row[14] else None, location='home')
            cell = Phone(number=row[15] if row[15] else None, location='cell')
            work = Phone(number=row[16] if row[16] else None, location='work')
            phones = [p for p in [home, cell, work] if p]
            user.phones.extend(phones)

            # Where do they work?
            work = Employment(name=row[19],
                              occupation=row[20],
                              status=row[21])
            user.employment.append(work)

            # Do they have any family?  Unfortunately the way kids were handled
            # in the past means that there's no reliable way to parse that
            # info and apply it to this new database.
            fam1 = Family(relation=row[22], name=row[23] if row[23] else None)
            fam2 = Family(relation=row[24], name=row[25] if row[25] else None)
            fam3 = Family(relation=row[26], name=row[27] if row[27] else None)
            fam4 = Family(relation=row[28], name=row[29] if row[29] else None)
            fam5 = Family(relation=row[30], name=row[31] if row[31] else None)
            family = [f for f in [fam1, fam2, fam3, fam4, fam5] if f]
            user.relations.extend(family)

            # Did they have any pets?
            def create_pet(rows):
                # If we don't have enough info to create one, don't.
                type, name, gender, age, altered, whathappened = rows
                if not type:
                    return
                p = Pet(type=type,
                        name=name if name else None,
                        gender=gender,
                        age=age if age else None,
                        altered=str_to_bool(altered) if altered else None,
                        whathappened=whathappened)
                return p

            pets = [p for p in map(create_pet, [row[42:48], row[48:54], row[54:60], row[60:66], row[66:72]]) if p]
            if pets:
                user.pets.extend(pets)

            # Now for the profile!
            p = Profile()
            p.free_feed = str_to_bool(row[72])
            p.who_cares = unicode(row[73].strip(), CODEC, 'ignore')
            p.home = unicode(row[74].strip(), CODEC, 'ignore')
            p.needs = unicode(row[75].strip(), CODEC, 'ignore')
            p.alone_time = unicode(row[76].strip(), CODEC, 'ignore')
            p.dog_kept_home = row[77].strip()
            p.dog_kept_away = row[78].strip()
            p.dog_door = row[79].strip()
            p.transport = unicode(row[80].strip(), CODEC, 'ignore')
            p.crate = unicode(row[81].strip(), CODEC, 'ignore')
            p.sleep = unicode(row[82].strip(), CODEC, 'ignore')
            p.why_ridgebacks = row[83].strip()
            p.before_pets = row[84].strip()
            p.expenses = row[85].strip()
            p.day_in_the_life = unicode(row[86].strip(), CODEC, 'ignore')
            p.dog_as_family = unicode(row[87].strip(), CODEC, 'ignore')
            p.activity_level = unicode(row[88].strip(), CODEC, 'ignore')
            p.away_care = unicode(row[89].strip(), CODEC, 'ignore')
            p.give_up = unicode(row[90].strip(), CODEC, 'ignore')
            p.housing = row[91]
            p.own_rent = row[92]
            p.landlord_proof = row[93]
            p.yard = row[94]
            p.fence = row[95]
            p.fence_details = unicode(row[96].strip(), CODEC, 'ignore')
            p.ridgeback_gender = row[98]
            p.ridgeback_age = row[99].strip()
            p.ridgeback_ridges = row[100]
            p.ridgeback_purebred = row[101]
            p.ridgeback_health_problems = row[102].strip()
            p.ridgeback_social_problems = row[103].strip()

            user.profile = p

            # Finally, try to tie this application to a dog, an admin, and the
            # user
            assignee = db.session.query(User).filter(User.role == 1).\
                                              filter(User.username == row[1].lower()).\
                                              first()
            app.assignee = assignee

            dog = db.session.query(Dog).filter(Dog.name == row[97].strip()).first()
            app.dog = dog
            app.applicant = user

            db.session.add(user)
            db.session.add(app)
            db.session.commit()  # Slower to do it here, but we need to get users added so we can query for them

    print "Processed %d apps." % (i + 1)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recreate',
                        help='Drop and re-create all tables.',
                        action='store_true')
    parser.add_argument('--dog-csv',
                        help='The csv file containing the Dog_info table.')
    parser.add_argument('--user-csv',
                        help='The csv file containing the auth table.')
    parser.add_argument('--app-csv',
                        help='The csv file containing the Apps table.')
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
    if args.app_csv:
        import_apps(args.app_csv)


if __name__ == '__main__':
    main()
