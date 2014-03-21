# Create a GeoJSON file that contains geometry data and rent data 
# for 2013 census area units.
# Store the rent data in a nested JSON dict of the form
# 2006 census area unit (AU) name -> property/domicile type 
# -> number bedrooms -> rent
from __future__ import print_function
import csv, json

# Input files
rent_csv = 'data/mean_rents.csv'
geodata_geojson = 'data/Auckland_AUs_2013.geojson'
aus_and_suburbs_csv = 'data/Auckland_AUs_2013_and_suburbs.csv'
AUCKLAND_RENT_REGIONS = {'Auckland', 'Franklin', 'Manukau', 'North Shore', 
  'Papakura', 'Rodney', 'Waitakere'}

# Output file
outfile = 'data/mean_rents_by_nbedrooms_by_au.json'

# Convert rent_csv data into a nested dictionary keyed by rent suburb
rent_by_nbedrooms_by_suburb = dict()
with open(rent_csv, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    reader.next() # Skip header row
    for row in reader:
        region, suburb, prop, nbedrooms, rent = row[:4] + [row[-1]]
        if region not in AUCKLAND_RENT_REGIONS or prop != 'Total':
            # Skip row
            continue
        if suburb not in rent_by_nbedrooms_by_suburb.keys():
            rent_by_nbedrooms_by_suburb[suburb] = {nbedrooms: rent}
        elif nbedrooms not in rent_by_nbedrooms_by_suburb[suburb].keys():
            rent_by_nbedrooms_by_suburb[suburb][nbedrooms] = rent

# Print rent suburbs for reference
suburbs = sorted(rent_by_nbedrooms_by_suburb.keys())
print('rent suburbs ({!s}): '.format(len(suburbs)))
for suburb in suburbs:
    print(suburb)
print()

# Print census AUs for reference
with open(geodata_geojson, 'rb') as json_file:
    geo = json.loads(json_file.read())

aus = sorted([feature['properties']['AU_NAME'] for feature in geo['features']])
print('aus ({!s}): '.format(len(aus)))
for au in aus:
    print(au)
print()

# Use aus_and_suburbs.csv to convert the dictionary keys 
# from rent suburb to AU 
rent_by_nbedrooms_by_au = dict()
with open(aus_and_suburbs_csv, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    reader.next() # Skip header row
    for row in reader:
        au, suburb = row
        if suburb:
            rent_by_nbedrooms_by_au[au] =\
              rent_by_nbedrooms_by_suburb[suburb]
        else:
            # No data
            rent_by_nbedrooms_by_au[au] = 'NA'

# Dump to JSON
with open(outfile, 'w') as json_file:
    json.dump(rent_by_nbedrooms_by_au, json_file)