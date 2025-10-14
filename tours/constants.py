# Constants for Bellavista Care Homes
# This file contains configuration data for all care home locations

# =============================================================================
# CARE HOME LOCATIONS
# =============================================================================

# Dictionary containing details for each Bellavista care home
# Used for location services and contact information
HOME_LOCATIONS = {
    'cardiff': {
        'name': 'Bellavista Cardiff',
        'address': 'Cardiff, Wales, UK',
        'coordinates': (51.4816, -3.1791),  # Latitude, Longitude
        'phone': '029 2000 0000'
    },
    'barry': {
        'name': 'Bellavista Barry',
        'address': 'Barry, Vale of Glamorgan, Wales, UK',
        'coordinates': (51.3998, -3.2826),  # Latitude, Longitude
        'phone': '01446 700 000'
    },
    'waverley': {
        'name': 'Waverley Care Centre',
        'address': 'Waverley, Wales, UK',
        'coordinates': (51.4850, -3.1750),  # Latitude, Longitude
        'phone': '029 2100 0000'
    },
    'college-fields': {
        'name': 'College Fields',
        'address': 'College Fields, Wales, UK',
        'coordinates': (51.4900, -3.1800),  # Latitude, Longitude
        'phone': '029 2200 0000'
    }
}

# =============================================================================
# CALCULATION CONSTANTS
# =============================================================================

# Average driving speed for travel time estimation (km/h)
# Used in the find_nearest_home function to estimate journey duration
AVERAGE_SPEED_KMH = 40