"""
TODO:

- Finish
- Move checks to test file
"""
import json
import csv
import os

from shapely.geometry import shape
from shapely.ops import transform
import pyproj

MASTER_SHAPES_FILE = 'data/shapes.geojson'
# Property field of the GeoJSON file MASTER_SHAPES_FILE under 
# which is stored the name of an area unit:
NAME_FIELD = 'AU2013_NAM' 
MASTER_RENTS_FILE = 'data/rents.csv'
REGIONS = {'auckland', 'canterbury', 'nelson', 'otago', 'waikato', 
  'wellington'}
MODES = ['walk', 'bicycle', 'car', 'transit']
COMMUTE_COST_PER_KM_BY_MODE = {'walk': 0, 'bicycle': 0, 'car': 0.274, 
  'transit': 0.218}

def load_json(filename):
    """
    Read the JSON file with the given filename, 
    decode its contents into a Python dictionary, and return the result.
    """
    with open(filename, 'r') as f:
        return json.load(f)

def dump_json(json_dict, filename):
    """
    Write the given decoded JSON dictionary to a JSON file with the given name.
    """
    with open(filename, 'w') as f:
        json.dump(json_dict, f)

def make_feature_collection(features):
    return {
      'type': 'FeatureCollection',
      'features': features,
    }

def filter(collection, prop, values):
    """
    Given a (decoded) GeoJSON feature collection, return a new 
    feature collection that comprises the features f for which
    ``f['properties'][prop]`` lies in the set/list ``values``.
    """
    features = [f for f in collection['features']
      if f['properties'][prop] in values]
    return make_feature_collection(features)

def pj_nztm(u, v, inverse=False):
    """
    Convert a WGS84 longitude-latitude pair to an NZTM coodinate pair.
    Do the inverse conversion if ``inverse == True``.

    EXAMPLES::

        >>> (u, v) = (174.739869, -36.840417)  # Auckland
        >>> x, y = convert_pj_nztm(u, v); x, y
        (1755136.3841240003, 5921417.890287282)
        >>> pj_nztm(x, y, inverse=True)
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

def point_to_tuple(p):
    """
    Convert the given Shapely point to an (x, y) tuple.
    """
    return (p.x, p.y)

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


class Region(object):
    """
    Represents a region of New Zealand (NZ).
    """
    def __init__(self, path, name=None):
        """
        The given path will house the data for this region, and
        it needs to initially contain a file called 'area_units.csv'
        that has a header row and has a first column containing
        all the names of the area units in this region.
        The names are a subset of the names listed in 
        ``MASTER_SHAPES_FILE`` under the property ``NAME_FIELD``.
        
        Derive the region name from ``path`` if no name is given.
        """
        self.path = path
        if name is None:
            self.name = path.rstrip('/').split('/')[-1]
        else:
            self.name = name

    def __repr__(self):
        result = []
        for k, v in self.__dict__.items():
            result.append('{!s}: {!s}'.format(k, v))
        return '\n'.join(result)

    def get_area_units(self):
        """
        Return the set of area unit names of this region.
        """
        path = os.path.join(self.path, 'area_units.csv')
        area_units = set()
        with open(path, 'r') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader) 
            for row in reader:
                area_units.add(row[0])
        return area_units

    def create_shapes(self):
        """
        Create a GeoJSON feature collection of the shapes  
        (polygons and multipolygons) of the area units of this region
        and save it to the file system.
        """
        path = os.path.join(self.path, 'shapes.geojson')
        collection = load_json(MASTER_SHAPES_FILE)
        area_units = self.get_area_units()
        new_collection = filter(collection, NAME_FIELD, area_units)
        dump_json(new_collection, path)

        # # Little check
        # A = area_units
        # B = get_prop_set(new_collection, 'AU2013_NAM')
        # success = (A == B)
        # print('  Got shapes for each AU?', success)
        # if not success:
        #     print('  Missing geodata for', A - B)

    def get_shapes(self):
        """
        Return a decoded GeoJSON feature collection of the shapes  
        (polygons and multipolygons) of the area units of this region.
        """
        path = os.path.join(self.path, 'shapes.geojson')
        with open(path, 'r') as f:
            return json.loads(f.read())

    def create_rents(self, max_bedrooms=5):
        """
        Read in the ``MASTER_RENTS_FILE``, get the section of it
        pertaining to this region, convert it to a nested dictionary,
        and save it as a JSON file.

        The dictionary structure is 
        area unit name -> number of bedrooms -> median weekly rent
        
        Only get data for dwellings with at most ``max_bedrooms`` bedrooms.
        """
        path = os.path.join(self.path, 'rents.json')

        # Initialize dictionary
        area_units = self.get_area_units()
        rent_by_num_bedrooms_by_area_unit =\
          {area_unit: {i: None for i in range(1, max_bedrooms + 1)} 
          for area_unit in area_units}

        # Get rents for this region
        with open(MASTER_RENTS_FILE, 'r') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader) 
            for row in reader:
                area_unit, num_bedrooms, count, rent = row[:4]
                if area_unit not in area_units or\
                  num_bedrooms not in\
                  [str(i) for i in range(max_bedrooms + 1)] or\
                  not rent:
                    # Skip row. 
                    # Note that null rents are already recorded in the output.
                    continue
                num_bedrooms = int(num_bedrooms)
                rent = int(rent)
                rent_by_num_bedrooms_by_area_unit[area_unit][num_bedrooms] =\
                  rent
        
        # Save
        dump_json(rent_by_num_bedrooms_by_area_unit, path)

        # # Little check
        # A = area_units
        # B = set(rent_by_num_bedrooms_by_area_unit.keys())
        # success = (A == B)
        # print('  Got rents for each AU?', success)
        # if not success:
        #     print('  Missing rents for', A - B)

    def create_centroids(self, digits=5):
        """
        Calculate the centroids of the area units of this region and 
        save them to a GeoJSON file and a CSV file.

        For the CSV file create a header row and data rows with the following
        columns:

        1. area unit name
        2. WGS84 longitude of area unit
        3. WGS84 latitude of area unit.

        Round all longitude and latitude entries to ``digits``
        decimal places.
        Note that 5 decimal places in longitude and latitude degrees gives
        a precision on the ground of about 1 meter; see
        `here <https://en.wikipedia.org/wiki/Decimal_degrees>`_ . 
        """
        geojson_path = os.path.join(self.path, 'centroids.geojson')
        csv_path = os.path.join(self.path, 'centroids.csv')

        collection = self.get_shapes()
        centroid_by_area_unit = {}
        for f in collection['features']:
            # Convert to Shapely object with NZTM coords
            poly = transform(pj_nztm, shape(f['geometry']))
            # Get centroid and convert to WGS84 coords
            centroid = transform(lambda x, y: pj_nztm(x, y, inverse=True),
              poly.centroid)
            # Round
            centroid = my_round(centroid.coords[0], digits)
            # Save
            area_unit = f['properties'][NAME_FIELD]
            centroid_by_area_unit[area_unit] = centroid

        # Write CSV and collect GeoJSON features
        features = []
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['2013 area unit name', 
              'WGS84 longitude of centroid of area unit',
              'WGS84 latitude of centroid of area unit'])
            for area_unit, centroid in sorted(centroid_by_area_unit.items()):
                # CSV row
                writer.writerow([area_unit, centroid[0], centroid[1]])
                # GeoJSON point feature for later
                feature = {
                  'type': 'Feature',
                  'geometry': {
                    'type': "Point",
                    'coordinates': centroid,
                   },
                  'properties': {
                    NAME_FIELD: area_unit,
                  }
                }
                features.append(feature)

        # Combine GeoJSON features and write to file
        geojson = make_feature_collection(features)
        dump_json(geojson, geojson_path)

    def get_centroids(self):
        """
        Return a dictionary with structure
        area unit -> WGS84 (lon, lat) coordinates of centroid.
        """
        path = os.path.join(self.path, 'centroids.geojson')
        collection = load_json(path)
        return {f['properties'][NAME_FIELD]: f['geometry']['coordinates']
          for f in collection['features']}

    # TODO: Finish this
    def create_fake_commute_costs(self, n=100):
        """
        Generate fake commute distance and time information for this region and 
        convert it into one JSON master file of daily commute costs and times. 
        More specifically, write to ``data/<region>/fake_commute_costs.json`` 
        the data ``{'index_by_name': index_by_name, 'matrix': M}``, where 
        ``index_by_name`` is a dictionary with structure
        area unit name -> row/column index in the lower-triangular half-matrix 
        ``M``, where ``M`` is encoded by a dictionary with structure
        mode -> list of lists of cost-time pairs 
        such that ``M[mode][i][j]`` equals the cost in dollars
        and the time in hours that it takes to travel round-trip by the given mode
        (specified in the list ``MODES``)
        from the centroid of the area unit with index ``i >= 0`` 
        to the centroid of the area unit with index ``j <= i``.
        
        The commute distance used is 
        ('walk', 'bicycle', 'car', 'transit') = (d, d, d, d)
        and the commute time used is (t*15, t*4, t, t), 
        where d and t come from ``get_bird_distance_and_time()``

        The ``name_field`` input is used to call 
        ``get_polygon_and_centroid_by_au_name()``.
        The ``n`` input is used to compute ``M[mode][i][i]`` by choosing 
        ``n`` points uniformly at random 
        from the polygon for area unit ``i`` and taking the median of the
        distances and times from each of these points to the polygon's centroid.
        """
        path = os.path.join(self.path, 'fake_commute_costs.json')
        
        centroid_by_area_unit = self.get_centroids()
        names = list(centroid_by_area_unit.keys())
        index_by_name = {name: i for (i, name) in enumerate(names)}
        n = len(names)

        # Initialize matrix
        M = {mode: [[(None, None) for j in range(n)] for i in range(n)] 
          for mode in MODES}

        # Calculate M
        for i in range(n):
            a = centroids_wgs84[i]
            for j in range(n):
                if j != i:
                    b = centroids_wgs84[j] 
                    distance, time = get_bird_distance_and_time(a, b)
                else:
                    # Get sample points in polyon
                    polygon = pc_by_name[names[i]][0]
                    sample_points = [pj_nztm(*point_to_tuple(point), 
                      inverse=True) for point in get_sample_points(polygon, n=n)]
                    distances, times = list(zip(*[get_bird_distance_and_time(point, a)
                      for point in sample_points]))
                    distance, time = (median(list(distances)), median(list(times)))
                distance = round(distance, 2)
                time = round(time, 2)
                M['walk'][i][j] = (distance, time*15)
                M['bicycle'][i][j] = (distance, time*4)
                M['car'][i][j] = (distance, time)
                M['transit'][i][j] = (distance, time)

        # Create a cost lower-half-matrix from M
        MM = {mode: [[(None, None) for j in range(i + 1)] for i in range(n)] 
          for mode in MODES}
        for mode in MODES:
            for i in range(n):
                for j in range(i + 1):
                    try:
                        distance = M[mode][i][j][0] + M[mode][j][i][0]
                        time = M[mode][i][j][1] + M[mode][j][i][1]
                        MM[mode][i][j] = (
                          round(COMMUTE_COST_PER_KM_BY_MODE[mode]*distance, 2),
                          round(time, 1)
                          )
                    except TypeError:
                        # Defaults to MM[mode][i][j] = (None, None) 
                        pass 

        data = {'index_by_name': index_by_name, 'matrix': MM}
        dump_json(data, prefix + 'fake_commute_costs.json')


if __name__ == '__main__':
    region = Region(path='data/nelson/')
    print('Creating files for region {!s}...'.format(region.name))
    print('  Shapes...')
    region.create_shapes()
    print('  Rents...')
    region.create_rents()
    print('  Centroids...')
    region.create_centroids()
    print(region.get_centroids())
    # print('  Fake commute costs...')
    # region.create_fake_commute_costs()
    # print('  Commute costs...')
    # region.create_commute_costs()
    # if region == 'auckland':
    #     add_fare_zones(region)
    #     improve_auckland_transit_commute_costs()