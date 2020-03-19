#
# List of tuples with country codes and country
# Examples from 'Fluent Python' by Luciano Ramalho

from pprint import pprint as pp

DIAL_CODES = [
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
    (62, 'Indonesia'),
    (55, 'Brazil'),
    (92, 'Pakistan'),
    (880, 'Bangladesh'),
    (234, 'Nigeria'),
    (7, 'Russia'),
    (81, 'Japan')]

if __name__ == '__main__':
    # Build a country->code dictionary using dictcomps
    country_code = {country: code for code, country in DIAL_CODES}
    print("-" * 25)
    pp(country_code, indent=4)
    # Build reverse code-> uppercase(country) using dictcomp
    print("-" * 25)
    pp({code:country.upper() for country, code in country_code.items()},
       indent=4)
    print("-" * 65)
    # Build reverse code-> uppercase(country) using dictcom
    # Filter code < 66
    pp({code:country.upper() for country, code in country_code.items() if code < 66},
       indent=4)

