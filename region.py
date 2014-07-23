"""
TODO:

- Finish
- Move checks to test file
"""

MASTER_SHAPES_FILE = 'data/shapes.geojson'
NAME_FIELD = 'AU2013_NAM'
MASTER_RENTS_FILE = 'data/rents.csv'
REGIONS = {'auckland', 'canterbury', 'nelson', 'otago', 'waikato', 
  'wellington'}
MODES = ['walk', 'bicycle', 'car', 'transit']
COMMUTE_COST_PER_KM_BY_MODE = {'walk': 0, 'bicycle': 0, 'car': 0.274, 
  'transit': 0.218}

# JSON/GeoJSON functions
def load_json(filename):
    """
    Read the JSON file with the given filename, 
    decode its contents into a Python dictionary, and return the result.
    """
    with open(filename, 'r') as f:
        return json.loads(f.read())

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

def get_prop_set(collection, prop):
    """
    Given a decoded GeoJSON feature collection, return 
    ``set(f['properties'][prop] for f in collection['features'])``
    """
    return set(f['properties'][prop] for f in collection['features'])

def get_slice(collection, prop, values):
    """
    Given a (decoded) GeoJSON feature collection, return a new 
    feature collection that comprises the features f for which
    ``f['properties'][prop]`` lies in the set/list ``values``.
    """
    features = [f for f in collection['features']
      if f['properties'][prop] in values]
    return make_feature_collection(features)

# Geography functions
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

# TODO: clean this up and get projection working
def geojson_to_shapely(feature, proj=None):
    """
    Given a GeoJSON polygon or multipolygon feature,
    return its corresponding Shapely object.
    If a non-None projection function is given as ``proj``,
    then use it to project the featuer's coordinates.
    For example, ``proj`` could be ``pj_nztm``.
    """
    ftype = feature['geometry']['type']
    assert ftype in ['Polygon', 'MultiPolygon'],
      "Feature must be a polygon or multipolygon"

    def coords_to_polygon(coords):
        if not coords:
            return Polygon()
        exterior = coords.pop(0)
        try:
            interior = coords.pop(0)
            interior = [interior]
        except IndexError:
            interior = []
        return Polygon(exterior, interior)

    coords = feature['geometry']['coordinates']
    if ftype == 'Polygon':
        result = coords_to_polygon(coords, pj_nztm)
    elif ftype == 'MultiPolygon':
        polygons = [coords_to_polygon(cs, pj_nztm)
          for cs in coords]
        result = unary_union(polygons)
    # Project points
    if proj is not None:
        continue
    return result


class Region(object):
    """
    Represents a region of New Zealand (NZ).
    """
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]

    def __unicode__(self):
        result = []
        for k, v in self.__dict__.items():
            result.append('{!s}: {!s}'.format(k, v))
        return '\n'.join(result)

    def get_area_units(self):
        """
        Return the set of area unit names of this region.
        """
        filename = self.path + 'area_units.csv'
        area_units = set()
        with open(filename, 'r') as f:
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
        collection = load_json(MASTER_SHAPES_FILE)
        area_units = self.get_area_units()
        new_collection = get_slice(collection, NAME_FIELD, area_units)
        dump_json(new_collection, self.path + 'shapes.geojson')

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
        filename = self.path + 'shapes.geojson'
        with open(filename, 'r') as f:
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
        dump_json(rent_by_num_bedrooms_by_area_unit, self.path + 'rents.json')

        # # Little check
        # A = area_units
        # B = set(rent_by_num_bedrooms_by_area_unit.keys())
        # success = (A == B)
        # print('  Got rents for each AU?', success)
        # if not success:
        #     print('  Missing rents for', A - B)

    def create_centroids(self, digits=5):
        """
        Create a GeoJSON and CSV file containing the centroids of the area
        units for a given region from ``REGIONS``.
        If ``region is None``, then create the two centroid files for all
        of New Zealand.

        For the CSV file create a header row and data rows with the following
        columns:

        1. area unit name
        2. WGS84 longitude of area unit
        3. WGS84 latitude of area unit.

        For the GeoJSON file, create feature collection of point features,
        one for each centroid.

        All longitude and latitude entries are rounded to ``digits``
        decimal places.
        Note that 5 decimal places in longitude and latitude degrees gives
        a precision on the ground of about 1 meter; see
        `here <https://en.wikipedia.org/wiki/Decimal_degrees>`_ . 
        """
        collection = self.get_shapes()
        pc_by_name = get_polygon_and_centroid_by_au_name(collection, 
          name_field=name_field)
        
        # Create CSV and GeoJSON
        features = []
        with open(self.path + 'centroids.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['2013 area unit name', 
              'WGS84 longitude of centroid of area unit',
              'WGS84 latitude of centroid of area unit'])
            for name, pc in sorted(pc_by_name.items()):
                centroid = my_round(pj_nztm(*point_to_tuple(pc[1]), inverse=True),
                  digits=digits)
                # CSV row
                writer.writerow([name, centroid[0], centroid[1]])
                # GeoJSON point feature for later
                feature = {
                  'type': 'Feature',
                  'geometry': {
                    'type': "Point",
                    'coordinates': list(centroid),
                   },
                  'properties': {
                    name_field: name,
                  }
                }
                features.append(feature)

        # Combine GeoJSON features and write to file
        geojson = make_feature_collection(features)
        dump_json(geojson, self.path + 'centroids.geojson')


if __name__ == '__main__':
    region = Region(path='data/nelson/')
    print('Creating files for %s...' % region)
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