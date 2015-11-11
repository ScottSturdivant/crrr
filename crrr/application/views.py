from datetime import datetime
from sqlalchemy.sql.expression import asc, desc
from flask import request, render_template, g, Blueprint
from flask.ext.mail import Message
from crrr import app, mail, db
from crrr.root.forms import Application
from crrr.root.models import App
from crrr.dogs.models import Dog
from crrr.admin.models import (
    User,
    Address,
    Profile,
    Pet,
    Employment,
    Family,
    Phone,
)

mod = Blueprint('application', __name__, url_prefix='/application')


def str_to_bool(foo):
    return True if foo.lower() in ['y', 'yes', 'true', '1'] else False


def _store_application(form):
    """Stores the POSTed form in the database."""
    app = App()

    # Look to see if this user has already submitted previous applications
    user = User.query.filter_by(email=form.email.data).first()
    if user is None:
        user = User(username=form.email.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password='changeme',
                    active=False)

    home = Address(location='home',
                   line_1=form.addr_1.data,
                   line_2=form.addr_2.data,
                   city=form.city.data,
                   state=form.state.data,
                   zip=form.zip_code.data,
                   duration=form.address_length.data)

    vet = Address(location='vet',
                  clinic=form.ref1_firstname.data,
                  vet_name=form.ref1_lastname.data,
                  line_1=form.ref1_address1.data,
                  line_2=form.ref1_address2.data,
                  city=form.ref1_city.data,
                  state=form.ref1_state.data,
                  zip=form.ref1_zip.data)

    phone = Phone(number=form.ref1_phone.data, location='work')
    vet.phones.append(phone)
    user.addresses.extend([home, vet])

    # Get the user's phone numbers
    home = Phone(number=form.phone_h.data, location='home')
    cell = Phone(number=form.phone_c.data, location='cell')
    work = Phone(number=form.phone_w.data, location='work')
    phones = [p for p in [home, cell, work] if p]
    user.phones.extend(phones)

    # Get their employment information
    work = Employment(name=form.employer.data,
                      occupation=form.occupation.data,
                      status=form.employment_type.data)
    user.employment.append(work)

    # Do they have any family?  Record all of their relationships.
    fam1 = Family(relation=form.relation1.data, name=form.name1.data)
    fam2 = Family(relation=form.relation2.data, name=form.name2.data)
    fam3 = Family(relation=form.relation3.data, name=form.name3.data)
    fam4 = Family(relation=form.relation4.data, name=form.name4.data)
    fam5 = Family(relation=form.relation5.data, name=form.name5.data)
    family = [f for f in [fam1, fam2, fam3, fam4, fam5] if f]
    user.relations.extend(family)

    # Did they have any pets?
    def _create_pet(form, pet_num):
        species = getattr(form, 'pet_{num}_species'.format(num=pet_num))
        name = getattr(form, 'pet_{num}_name'.format(num=pet_num))
        gender = getattr(form, 'pet_{num}_sex'.format(num=pet_num))
        age = getattr(form, 'pet_{num}_age'.format(num=pet_num))
        altered = getattr(form, 'pet_{num}_altered'.format(num=pet_num))
        whathappened = getattr(form, 'pet_{num}_whathappened'.format(num=pet_num))
        p = Pet(type=species.data,
                name=name.data,
                gender=gender.data,
                age=age.data,
                altered=str_to_bool(altered.data),
                whathappened=whathappened.data)
        return p
    pets = [_create_pet(form, i) for i in range(1, 6)]
    pets = [p for p in pets if p]
    if pets:
        user.pets.extend(pets)

    # Now for their profile, aka the guts of the application
    p = Profile(free_feed=str_to_bool(form.freefeed.data),
                who_cares=form.whocares.data,
                home=form.home.data,
                needs=form.needs.data,
                alone_time=form.alonetime.data,
                dog_kept_home=str(form.dogkepthome.data),
                dog_kept_away=str(form.dogkeptaway.data),
                dog_door=form.dogdoor.data,
                transport=form.transport.data,
                crate=form.crate.data,
                sleep=form.sleep.data,
                why_ridgebacks=str(form.whyridgebacks.data),
                before_pets=form.before.data,
                expenses=form.expenses.data,
                day_in_the_life=form.dayinthelife.data,
                dog_as_family=form.dogasfamily.data,
                activity_level=form.activitylevel.data,
                away_care=form.awaycare.data,
                give_up=form.giveup.data,
                housing=form.housing.data,
                own_rent=form.ownrent.data,
                landlord_proof=form.landlordproof.data,
                yard=form.yard.data,
                fence=form.fence.data,
                fence_details=form.fencedetails.data,
                ridgeback_gender=form.ridgebackgender.data,
                ridgeback_age=form.ridgebackage.data,
                ridgeback_ridges=form.ridgebackridges.data,
                ridgeback_purebred=form.ridgebackpurebred.data,
                ridgeback_health_problems=form.ridgebackhealthproblems.data,
                ridgeback_social_problems=form.ridgebacksocialproblems.data)
    user.profile = p

    # Assign this application to an admin
    app.assignee = User.query.filter_by(role=1).first()

    # If they specified a particular dog, associate it.
    app.dog = Dog.query.filter_by(name=form.ridgebackname.data).first()

    # Now tie up the associations and store in the db
    app.applicant = user
    db.session.add(user)
    db.session.add(app)
    db.session.commit()


@mod.route('/all/')
def all(showarchivedapps=None, dateasc=None):
    q = App.query
    if not showarchivedapps:
        q = q.filter(App.archive == False)  # noqa
    if dateasc:
        q = q.order_by(asc(App.submittal_date))
    else:
        q = q.order_by(desc(App.submittal_date))
    apps = q.all()
    return render_template('application/all.html', apps=apps)


@mod.route('/', methods=['GET', 'POST'])
def apply():
    g.application = True
    g.title = "CRRR - Application"
    form = Application(ridgebackname=request.args.get('dog'))
    if form.validate_on_submit():
        _store_application(form)
        submitted_at = datetime.now().strftime("%B %d, %Y, %I:%M %p")
        subject = '{} {} Application Submittal'.format(
            form.first_name.data,
            form.last_name.data
        )
        sender = app.config.get('CRRR_EMAIL')
        msg = Message(subject,
                      sender=sender,
                      recipients=[sender, form.email.data],
                      html=render_template('root/application_email.html',
                                           form=form,
                                           submitted_at=submitted_at)
                      )
        mail.send(msg)
        return render_template('root/application.html')
    return render_template('root/application.html', form=form)
