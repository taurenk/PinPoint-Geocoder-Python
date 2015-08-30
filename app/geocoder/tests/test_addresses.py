__author__ = 'Tauren'

test_address_dict = {
    # Normal Address
    '6 Caputo Drive Manorville NY 11949': {
        'number': '6',
        'line_1': 'CAPUTO DR',
        'line_2': '',
        'city': 'MANORVILLE',
        'state': 'NY',
        'zip': '11949'
    },

    # view + drive == street types
    '1 Canal View Dr, Center Moriches, NY 11934': {
        'number': '1',
        'line_1': 'CANAL VIEW DR',
        'line_2': '',
        'city': 'CENTER MORICHES',
        'state': 'NY',
        'zip': '11934'
    },

    # hwy + direction in city
    '492 Montauk Hwy, East Moriches, NY 11940': {
        'number': '492',
        'line_1': 'Montauk Hwy',
        'line_2': '',
        'city': 'EAST MORICHES',
        'state': 'NY',
        'zip': '11940'
    },

    # Just plain hard.
    '1400 Av of the Americas New York': {
        'number': '1400',
        'line_1': 'AVE OF THE AMERICAS',
        'line_2': '',
        'city': 'NEW YORK CITY',
        'state': 'NY',
        'zip': ''
    },

    '1400 Avenue of the Americas, New York, NY 10019': {
        'number': '1400',
        'line_1': 'AVE OF THE AMERICAS',
        'line_2': '',
        'city': 'NEW YORK CITY',
        'state': 'NY',
        'zip': '10019'
     }
}
