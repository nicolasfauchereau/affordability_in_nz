# Create a JSON file that contains a matrix of travel distance and
# and travel time estimates between the centroids of 2013 census area units 
# (AUs). 
# Store the matrix in a nested JSON dict of the form
# AU name -> AU name -> (distance in km, time in minutes)
from __future__ import print_function
import pyproj, shapely, json

# Input file
geodata_geojson = 'data/Auckland_AUs_2013.geojson'
# Output file
outfile = 'data/orig_dest_matrix.json'

def my_round(x, digits=5):
    """
    Round the floating point number or list/tuple of floating point
    numbers to ``digits`` number of digits.
    Calls Python's ``round()`` function.

    EXAMPLES::

        >>> print(my_round(1./7, 6))
        0.142857
        >>> print(my_round((1./3, 1./7), 6))
        (0.333333, 0.142857)
       
    """
    try:
        result = round(x, digits)
    except TypeError:
        result = [my_round(xx, digits) for xx in x]
        if isinstance(x, tuple):
            result = tuple(result)
    return result 

def wgs84_to_nztm(u, v, inverse=False):
    """
    Convert a WGS84 longitude-latitude pair to an NZTM coodinate pair.
    Do the inverse conversion if ``inverse == True``.

    EXAMPLES::

        >>> (u, v) = (174.739869, -36.840417)  # Auckland
        >>> x, y = convert_wgs84_to_nztm(u, v); x, y
        (1755136.3841240003, 5921417.890287282)
        >>> wgs84_to_nztm(x, y, inverse=True)
        (174.73986900000267, -36.84041699999844)
    """
    # EPSG 4326, http://spatialreference.org/ref/epsg/4326/
    wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    # EPSG 2193, http://spatialreference.org/ref/epsg/2193/
    nztm = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=173 +k=0.9996 +x_0=1600000 +y_0=10000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs') 

    if not inverse:
        x, y = pyproj.transform(wgs84, nztm, u, v)
    else:
        x, y = pyproj.transform(nztm, wgs84, u, v)
    return x, y

def main():
    """
    Convert
    """
    from shapely.geometry import Polygon, MultiPolygon
    from shapely.ops import unary_union

    centroid_by_AU = dict()
    # Collect AUs and centroids
    with open(geodata_geojson, 'rb') as json_file:
        collection = json.loads(json_file.read())
        for feature in collection['features']:
            au = feature['properties']['AU_NAME']
            # Get centroid in NZTM coordinates
            if feature['geometry']['type'] == 'Polygon':
                coords = feature['geometry']['coordinates'][0]
                coords = [wgs84_to_nztm(*c) for c in coords]
                centroid = Polygon(coords).centroid
            elif feature['geometry']['type'] == 'MultiPolygon':
                polygons = [Polygon([wgs84_to_nztm(*c) for c in coords]) 
                  for coords in feature['geometry']['coordinates'][0]]
                centroid = unary_union(polygons).centroid
            else:
                print('This problematic feature is a', 
                  feature['geometry']['type'])
            centroid_by_AU[au] = centroid

# print()

# # Use aus_and_suburbs.csv to convert the dictionary keys 
# # from rent suburb to AU 
# rent_by_nbedrooms_by_au = dict()
# with open(aus_and_suburbs_csv, 'rb') as csv_file:
#     reader = csv.reader(csv_file)
#     reader.next() # Skip header row
#     for row in reader:
#         au, suburb = row
#         if suburb:
#             rent_by_nbedrooms_by_au[au] =\
#               rent_by_nbedrooms_by_suburb[suburb]
#         else:
#             # No data
#             rent_by_nbedrooms_by_au[au] = 'NA'

# # Dump to JSON
# with open(outfile, 'w') as json_file:
#     json.dump(rent_by_nbedrooms_by_au, json_file)

if __name__ == '__main__':
     main() 