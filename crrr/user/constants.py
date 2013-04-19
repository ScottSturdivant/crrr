# user roles
USER  = 0
ADMIN = 1
GOD   = 2
ROLES = {
    USER:  'user',
    ADMIN: 'admin',
    GOD:   'god',
}

# user address locations
HOME = 0
WORK = 1
VET  = 2
LOCATIONS = {
    HOME: 'home',
    WORK: 'work',
    VET:  'vet',
}

# user employment status
FULL = 0
PART = 1
NONE = 2
EMPLOYMENT_STATUS = {
    FULL: 'full time',
    PART: 'part time',
    NONE: 'unemployed',
}

# user family relationships
NA       = 0  # Important for this to be 0
SPOUSE   = 1
PARTNER  = 2
BROTHER  = 3
SISTER   = 4
SON      = 5
DAUGHTER = 6
FRIEND   = 7
OTHER    = 8
RELATIONSHIPS = {
    NA:       'N/A',
    SPOUSE:   'spouse',
    PARTNER:  'partner',
    BROTHER:  'brother',
    SISTER:   'sister',
    SON:      'son',
    DAUGHTER: 'daughter',
    FRIEND:   'friend',
    OTHER:    'other',
}

# user phone types
HOME = 0
WORK = 1
CELL = 2
PHONES = {
    HOME: 'home',
    WORK: 'work',
    CELL: 'cell',
}

# user home type
HOUSE     = 0
TOWNHOME  = 1
APARTMENT = 2
CONDO     = 3
MOBILE    = 4
RANCH     = 5
FARM      = 6
DUPLEX    = 7
OTHER     = 8
HOME_TYPES = {
    HOUSE:     'house',
    TOWNHOME:  'townhome',
    APARTMENT: 'apartment',
    CONDO:     'condo',
    MOBILE:    'mobile home',
    RANCH:     'ranch',
    FARM:      'farm',
    DUPLEX:    'duplex',
    OTHER:     'other',
}

# user ownership status
OWN  = 0
RENT = 1
OWNERSHIP = {
    OWN:  'own',
    RENT: 'rent',
}

# user landlord proof
YES = 0
NO  = 1
NA  = 2
LANDLORD_PROOF = {
    YES: 'yes',
    NO:  'no',
    NA:  'N/A'
}

# user ridgeback gender preference
EITHER = 0
MALE   = 1
FEMALE = 2
GENDER_PREFERENCE = {
    EITHER: 'either',
    MALE:   'male',
    FEMALE: 'female',
}

# user ridgeback ridged preference
EITHER    = 0
RIDGED    = 1
RIDGELESS = 2
RIDGED_PREFERENCE = {
    EITHER:    'either',
    RIDGED:    'ridged',
    RIDGELESS: 'ridgeless',
}

# user ridgeback purebred preference
EITHER   = 0
PUREBRED = 1
MIXED    = 2
PUREBRED_PREFERENCE = {
    EITHER:   'either',
    PUREBRED: 'purebred',
    MIXED:    'mixed',
}
