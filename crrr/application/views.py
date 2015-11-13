from datetime import datetime
from sqlalchemy.sql.expression import asc, desc
from flask import request, render_template, g, Blueprint
from flask.ext.mail import Message
from flask.ext.login import login_required
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
@login_required
def all():
    q = App.query
    if not request.args.get('showarchivedapps'):
        q = q.filter(App.archive == False)  # noqa
    if request.args.get('dateasc'):
        q = q.order_by(asc(App.submittal_date))
    else:
        q = q.order_by(desc(App.submittal_date))
    apps = q.all()
    return render_template('application/all.html', apps=apps)


@mod.route('/<int:id>/')
@login_required
def view(id):
    app = App.query.get_or_404(id)
    user = app.applicant
    home_addr = [addr for addr in user.addresses if addr.location == 'home'][0]
    vet_addr = [addr for addr in user.addresses if addr.location == 'vet'][0]
    home_phone = [p for p in user.phones if p.location == 'home'][0]
    cell_phone = [p for p in user.phones if p.location == 'cell'][0]
    work_phone = [p for p in user.phones if p.location == 'work'][0]
    work = user.employment[0]

    kwargs = dict(
        first_name=user.first_name,
        last_name=user.last_name,
        addr_1=home_addr.line_1,
        addr_2=home_addr.line_2,
        city=home_addr.city,
        state=home_addr.state,
        zip_code=home_addr.zip,
        address_length=home_addr.duration,
        email=user.email,
        phone_h=home_phone.number,
        phone_c=cell_phone.number,
        phone_w=work_phone.number,
        employer=work.name,
        occupation=work.occupation,
        employment_type=work.status,
        kids=user.profile.kid_info,
        ref1_firstname=vet_addr.clinic,
        ref1_lastname=vet_addr.vet_name,
        ref1_address1=vet_addr.line_1,
        ref1_address2=vet_addr.line_2,
        ref1_city=vet_addr.city,
        ref1_state=vet_addr.state,
        ref1_zip=vet_addr.zip,
        ref1_phone=vet_addr.phones[0].number,
        # Profile information..
        freefeed=user.profile.free_feed,
        whocares=user.profile.who_cares,
        home=user.profile.home,
        needs=user.profile.needs,
        alonetime=user.profile.alone_time,
        dogkepthome=user.profile.dog_kept_home.split(','),
        dogkeptaway=user.profile.dog_kept_away.split(','),
        dogdoor=user.profile.dog_door,
        transport=user.profile.transport,
        crate=user.profile.crate,
        sleep=user.profile.sleep,
        whyridgebacks=user.profile.why_ridgebacks.split(','),
        before=user.profile.before_pets,
        expenses=user.profile.expenses,
        dayinthelife=user.profile.day_in_the_life,
        dogasfamily=user.profile.dog_as_family,
        activitylevel=user.profile.activity_level,
        awaycare=user.profile.away_care,
        giveup=user.profile.give_up,
        housing=user.profile.housing,
        ownrent=user.profile.own_rent,
        landlordproof=user.profile.landlord_proof,
        yard=user.profile.yard,
        fence=user.profile.fence,
        fencedetails=user.profile.fence_details,
        ridgebackname=app.dog.name if app.dog else None,
        ridgebackgender=user.profile.ridgeback_gender,
        ridgebackage=user.profile.ridgeback_age,
        ridgebackridges=user.profile.ridgeback_ridges,
        ridgebackpurebred=user.profile.ridgeback_purebred,
        ridgebackhealthproblems=user.profile.ridgeback_health_problems,
        ridgebacksocialproblems=user.profile.ridgeback_social_problems,
    )
    # Set the relationships
    for i, r in enumerate(user.relations):
        kwargs.update({
            'relation{}'.format(i + 1): r.relation,
            'name{}'.format(i + 1): r.name
        })

    # Set the pet information
    for i, pet in enumerate(user.pets):
        kwargs.update({
            'pet_{}_species'.format(i + 1): pet.type,
            'pet_{}_name'.format(i + 1): pet.name,
            'pet_{}_sex'.format(i + 1): pet.gender,
            'pet_{}_age'.format(i + 1): pet.age,
            'pet_{}_altered'.format(i + 1): pet.altered,
            'pet_{}_whathappened'.format(i + 1): pet.whathappened,
        })
    form = Application(**kwargs)
    return render_template('application/view.html', form=form)


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
