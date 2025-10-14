"""
Constants for Bellavista Care Homes locations
"""

# Home locations with coordinates (latitude, longitude) and contact info
HOME_LOCATIONS = {
    'cardiff': {
        'name': 'Bellavista Cardiff',
        'address': 'Cardiff, Wales, UK',
        'coordinates': (51.4816, -3.1791),  # Approximate coordinates for Cardiff
        'phone': '029 2000 0000'
    },
    'barry': {
        'name': 'Bellavista Barry',
        'address': 'Barry, Vale of Glamorgan, Wales, UK',
        'coordinates': (51.3998, -3.2826),  # Approximate coordinates for Barry
        'phone': '01446 700 000'
    },
    'waverley': {
        'name': 'Waverley Care Centre',
        'address': 'Waverley, Wales, UK',
        'coordinates': (51.4850, -3.1750),  # Approximate coordinates near Cardiff
        'phone': '029 2100 0000'
    },
    'college-fields': {
        'name': 'College Fields',
        'address': 'College Fields, Wales, UK',
        'coordinates': (51.4900, -3.1800),  # Approximate coordinates near Cardiff
        'phone': '029 2200 0000'
    }
}

# Average driving speed in km/h for duration estimation
AVERAGE_SPEED_KMH = 40
