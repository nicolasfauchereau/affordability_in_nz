# Create a GeoJSON file that contains geometry data and rent data 
# for 2006 census area units.
# Store the rent data in a nested JSON dict of the form
# 2006 census area unit (AU) name -> property/domicile type 
# -> number bedrooms -> rent
from __future__ import print_function
import csv, json

# Input files
rent_csv = 'data/mean_rents_auckland_2013_q3.csv'
geodata_geojson = 'data/AU_TA_Auckland_CC.geojson'
aus_and_suburbs_csv = 'data/aus_and_suburbs.csv'

# Output file
unified_geojson = 'data/AU_TA_Auckland_CC_with_rents.geojson'

# Convert rent_csv data into a nested dictionary keyed by rent suburb
rent_by_nbedrooms_by_property_by_suburb = dict()
with open(rent_csv, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    reader.next() # Skip header row
    for row in reader:
        region, au, prop, nbedrooms, rent = row
        if prop == 'Total':
            # Skip aggregated suburb rent
            continue
        if au not in rent_by_nbedrooms_by_property_by_suburb.keys():
            rent_by_nbedrooms_by_property_by_suburb[au] =\
              {prop: {nbedrooms: rent}}
        elif prop not in rent_by_nbedrooms_by_property_by_suburb[au].keys():
            rent_by_nbedrooms_by_property_by_suburb[au][prop] =\
              {nbedrooms: rent}
        elif nbedrooms not in rent_by_nbedrooms_by_property_by_suburb[au][
          prop].keys():
            rent_by_nbedrooms_by_property_by_suburb[au][prop][nbedrooms] = rent

# # Print rent suburbs for reference
# suburbs = sorted(rent_by_nbedrooms_by_property_by_suburb.keys())
# print('rent suburbs ({!s}): '.format(len(suburbs)))
# for suburb in suburbs:
#     print(suburb)
# print()

# Use aus_and_suburbs.csv to convert the dictionary keys 
# from rent suburb to AU 
rent_by_nbedrooms_by_property_by_au = dict()
with open(aus_and_suburbs_csv, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    reader.next() # Skip header row
    for row in reader:
        au, suburb = row
        if suburb:
            rent_by_nbedrooms_by_property_by_au[au] =\
              rent_by_nbedrooms_by_property_by_suburb[suburb]
        else:
            # No data
            rent_by_nbedrooms_by_property_by_au[au] = 'NA'

# # Print census AUs
# with open(geodata_geojson, 'rb') as json_file:
#     geo = json.loads(json_file.read())

# aus = sorted([feature['properties']['AU_NAME'] for feature in geo['features']])
# print('aus ({!s}): '.format(len(aus)))
# for au in aus:
#     print(au)
# print()

# Add rent data to geometry data from geodata_geojson 
# and save the result to unified_geojson
with open(geodata_geojson, 'rb') as json_file:
    geodata = json.load(json_file)

for feature in geodata['features']:
    props = feature['properties']
    props['rent_by_nbedrooms_by_property'] =\
      rent_by_nbedrooms_by_property_by_au[props['AU_NAME']]

with open(unified_geojson, 'w') as json_file:
    json.dump(geodata, json_file)