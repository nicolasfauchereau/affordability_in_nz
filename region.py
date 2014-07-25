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

def distance(lon1, lat1, lon2, lat2):
    """
    Given two (longitude, latitude) points in degrees, 
    compute their great circle distance in km on a spherical Earth of 
    radius 6371 km.  
    Use the haversine formula.
    """
    from math import radians, sin, cos, sqrt, asin

    R = 6371
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2*R*asin(sqrt(h))

def get_bird_distance_and_time(a, b):
    """
    Given a list of pairs WGS84 longitude-latitude points ``a`` and ``b``, 
    return the distance in kilometers and time in hours of the quickest 
    path from  ``a`` to ``b`` as the bird flies (at 40 kph).
    """
    d = distance(a[0], a[1], b[0], b[1])
    return d, d/40


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
        save them to a GeoJSON file.

        Round all longitude and latitude entries to ``digits``
        decimal places.
        Note that 5 decimal places in longitude and latitude degrees gives
        a precision on the ground of about 1 meter; see
        `here <https://en.wikipedia.org/wiki/Decimal_degrees>`_ . 
        """
        path = os.path.join(self.path, 'centroids.geojson')

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

        # Collect GeoJSON features
        features = [
          {
            'type': 'Feature',
            'geometry': {
              'type': "Point",
              'coordinates': centroid,
             },
            'properties': {
              NAME_FIELD: area_unit,
            }
          }
          for area_unit, centroid in centroid_by_area_unit.items()]

        # Combine GeoJSON features and write to file
        geojson = make_feature_collection(features)
        dump_json(geojson, path)

    def get_centroids(self):
        """
        Return a dictionary with structure
        area unit -> WGS84 (lon, lat) coordinates of centroid.
        """
        path = os.path.join(self.path, 'centroids.geojson')
        collection = load_json(path)
        return {f['properties'][NAME_FIELD]: f['geometry']['coordinates']
          for f in collection['features']}

    def create_fake_commute_costs(self):
        """
        Generate fake commute distance and time information for 
        this region and save it to a JSON file.
        The file data is a dictionary 
        ``{'index_by_name': index_by_name, 'matrix': M}``, where 
        ``index_by_name`` is a dictionary with structure
        area unit name -> row/column index in the lower-triangular half-matrix 
        ``M``, where ``M`` is encoded by a dictionary with structure
        mode -> list of lists of cost-time pairs 
        such that ``M[mode][i][j]`` equals the cost in dollars
        and the time in hours that it takes to travel round-trip by the 
        given mode (specified in the list ``MODES``)
        from the centroid of the area unit with index ``i >= 0`` 
        to the centroid of the area unit with index ``j <= i``.
        
        The commute distance used is 
        ('walk', 'bicycle', 'car', 'transit') = (d, d, d, d)
        and the commute time used is (t*15, t*4, t, t), 
        where d and t come from ``get_bird_distance_and_time()``
        """
        path = os.path.join(self.path, 'fake_commute_costs.json')
        
        centroid_by_name = self.get_centroids()
        names = list(centroid_by_name.keys())
        index_by_name = {name: i for (i, name) in enumerate(names)}
        name_by_index = {i: name for (i, name) in enumerate(names)}
        n = len(names)

        # Initialize matrix M
        M = {mode: [[(None, None) for j in range(n)] for i in range(n)] 
          for mode in MODES}

        # Calculate M
        for i in range(n):
            i_name = name_by_index[i]
            a = centroid_by_name[i_name]
            for j in range(n):
                j_name = name_by_index[j]
                b = centroid_by_name[j_name] 
                distance, time = get_bird_distance_and_time(a, b)
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

        # Save
        data = {'index_by_name': index_by_name, 'matrix': MM}
        dump_json(data, path)

    def get_commutes(self, mode='walk'):
        """
        Read the CSV file that stores the commute data for this
        region and the given mode (which lies in ``MODES``) and
        return a dictionary with the structure

        (origin area unit, destination area unit) -> (distance, time).

        The distance and time are measured in the same units 
        as those in the file, namely kilometers and hours,
        respectively.

        Return ``None`` if the commutes file does not exist.
        """
        assert mode in MODES,\
          "Mode must be in {!s}".format(MODES)

        path = os.path.join(self.path, mode + '_commutes.csv')
        if not os.path.isfile(path):
            return None

        M = {}
        with open(path, 'r') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader) 
            for row in reader:
                o_name, d_name, distance, time = row
                if distance:
                    distance = float(distance)
                else:
                    distance = None
                if time:
                    time = float(time)
                else:
                    time = None
                M[(o_name, d_name)] = (distance, time)
        return M

    def create_commute_costs(self):
        """
        Consolidate the data in the commute CSV files for this region and 
        save it into one JSON master file of daily commute cost and time. 
        More specifically, save the dictionary 
        ``{'index_by_name': index_by_name, 'matrix': M}``, where 
        ``index_by_name`` is a dictionary with structure
        area unit name -> row/column index in the lower-triangular half-matrix 
        ``M``, where ``M`` is encoded by a dictionary with structure
        mode -> list of lists of cost-time pairs 
        such that ``M[mode][i][j]`` equals the cost in dollars
        and the time in hours that it takes to travel round-trip by the 
        given mode (specified in the list ``MODES``)
        from the centroid of the area unit with index ``i >= 0`` 
        to the centroid of the area unit with index ``j <= i``.
        """
        path = self.path + 'commute_costs.json'
    
        # Get area units
        names = self.get_area_units()
        index_by_name = {name: i for (i, name) in enumerate(names)}
        n = len(names)

        # Create a commutes matrix M
        M = {mode: [[(None, None) for j in range(n)] for i in range(n)] 
          for mode in MODES}
        for mode in MODES:
            commutes = self.get_commutes(mode)
            if commutes is None:
                continue
            for (o_name, d_name), (distance, time) in commutes.items():
                # Save to matrix
                M[mode][index_by_name[o_name]][index_by_name[d_name]] =\
                  (distance, time)

        # Use M to create a cost lower-triangular half-matrix MM
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
                          round(time, 2)
                          )
                    except TypeError:
                        # Defaults to MM[mode][i][j] = (None, None) 
                        pass 

        # Write to file
        data = {'index_by_name': index_by_name, 'matrix': MM}
        dump_json(data, path)

if __name__ == '__main__':
    region = Region(path='data/nelson/')
    print('Creating files for region {!s}...'.format(region.name))
    print('  Shapes...')
    region.create_shapes()
    print('  Rents...')
    region.create_rents()
    print('  Centroids...')
    region.create_centroids()
    print('  Fake commute costs...')
    region.create_fake_commute_costs()
    print('  Commute costs...')
    region.create_commute_costs()
    # if region == 'auckland':
    #     add_fare_zones(region)
    #     improve_auckland_transit_commute_costs()