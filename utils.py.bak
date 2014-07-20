# Some utility functions
from __future__ import print_function, division
import datetime as dt 
import json, csv

import pyproj
import shapely
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.geometry.polygon import LinearRing
from shapely.ops import unary_union

MASTER_SHAPES_FILE = 'data/au_shapes.geojson'
MASTER_RENTS_FILE = 'data/au_rents.csv'
REGIONS = {'auckland', 'canterbury', 'nelson', 'otago', 'waikato', 
  'wellington'}
MODES = ['walk', 'bicycle', 'car', 'transit']
COMMUTE_COST_PER_KM_BY_MODE = {'walk': 0, 'bicycle': 0, 'car': 0.274, 
  'transit': 0.218}

def get_au_names(filename, header=True):
    """
    Given a CSV file with initial columns
    
    1. area unit name
    2. area unit code 

    return the set of all area unit names.
    If ``header == True``, then skip the first line 
    of the CSV.
    """
    au_names = set()
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        if header:
            # Skip header row
            reader.next() 
        for row in reader:
            au_names.add(row[0])
    return au_names
            
def load_json(filename):
    """
    Read the JSON file with the given filename, 
    decode its contents into a Python dictionary, and return the result.
    """
    with open(filename, 'rb') as f:
        return json.loads(f.read())

def dump_json(json_dict, filename):
    """
    Write the given decoded JSON dictionary to a JSON file with the given name.
    """
    with open(filename, 'w') as f:
        json.dump(json_dict, f)

# GeoJSON data functions
def features_to_feature_collection(features):
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

def slice_collection(collection, prop, values):
    """
    Given a (decoded) GeoJSON feature collection, return a new 
    feature collection that comprises the features f for which
    ``f['properties'][prop]`` lies in the set/list ``values``.
    """
    features = [f for f in collection['features']
      if f['properties'][prop] in values]
    return features_to_feature_collection(features)

def create_shapes(region, name_field='AU2013_NAM'):
    """
    Create the GeoJSON file comprising the AU shapes for a given region 
    from ``REGIONS``.
    """
    prefix = 'data/%s/' % region
    collection = load_json(MASTER_SHAPES_FILE)
    au_names = get_au_names(prefix + 'au_names.csv')
    new_collection = slice_collection(collection, name_field, au_names)
    dump_json(new_collection, prefix + 'au_shapes.geojson')

    # Little check
    A = au_names
    B = get_prop_set(new_collection, 'AU2013_NAM')
    success = (A == B)
    print('  Got shapes for each AU?', success)
    if not success:
        print('  Missing geodata for', A - B)

# Rent data functions
def create_rents(region, max_bedrooms=5, header=True):
    """
    Given the name of a CSV file in which each row contains as its first
    several entries
    
        1. area unit name
        2. number of bedrooms in dwelling
        3. count
        4. median weekly rent paid,
    
    return a nested dictionary of median weekly rent paid by number of
    bedrooms by area unit name.
    More specifically, the keys of the dictionary are the strings in the
    set/list ``au_names`` and each corresponding value in a dictionary with
    key-value pair (number of bedrooms, median weekly rent paid for a
    dwelling with that number of bedrooms in the given area unit).
    Only get data for dwellings with at most ``max_bedrooms`` bedrooms.
    If ``header == True``, then skip the first row of the CSV file.
    """
    prefix = 'data/%s/' % region

    # Initialize output
    au_names = get_au_names(prefix + 'au_names.csv')
    rent_by_num_bedrooms_by_au_name =\
      {au_name: {i: None for i in range(1, max_bedrooms + 1)} 
      for au_name in au_names}
    with open(MASTER_RENTS_FILE, 'rb') as f:
        reader = csv.reader(f)
        if header:
            # Skip header row
            reader.next() 
        for row in reader:
            au_name, num_bedrooms, count, rent = row[:4]
            if au_name not in au_names or\
              num_bedrooms not in [str(i) for i in range(max_bedrooms + 1)] or\
              not rent:
                # Skip row. 
                # Note that null rents are already recorded in the output.
                continue
            num_bedrooms = int(num_bedrooms)
            rent = int(rent)
            rent_by_num_bedrooms_by_au_name[au_name][num_bedrooms] = rent
    
    # Write to file
    dump_json(rent_by_num_bedrooms_by_au_name, prefix + 'au_rents.json')

    # Little check
    A = au_names
    B = set(rent_by_num_bedrooms_by_au_name.keys())
    success = (A == B)
    print('  Got rents for each AU?', success)
    if not success:
        print('  Missing rents for', A - B)

# Centroid data functions
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

def coords_to_polygon(coords, proj=None):
    """
    Given a list ``f['geometry']['coordinates']`` 
    of coordinates from a decoded GeoJSON polygon feature ``f``,
    return the corresponding Shapely polygon.
    If ``proj` is not ``None``, then project the coordinates
    first via the projection ``proj``.
    For example, ``proj`` could be ``pj_nztm``.
    """
    if not coords:
        return Polygon()
    exterior = coords.pop(0)
    if proj:
        exterior = [proj(*point) for point in exterior]
    try:
        interior = coords.pop(0)
        if proj:
            interior = [proj(*point) for point in interior]
        interior = [interior]
    except IndexError:
        interior = []
    return Polygon(exterior, interior)

def point_to_tuple(p):
    """
    Convert the given Shapely point to an (x, y) tuple.
    """
    return (p.x, p.y)

def get_polygon_and_centroid_by_au_name(collection, name_field='AU2013_NAM'):
    """
    Given a decoded GeoJSON feature collection of (multi)polygons in 
    WGS84 coordinates, each of which has a 
    name specified in ``feature['properties'][name_field]``. 
    Return a dictionary with the key-value pairs (polygon name, 
    (polygon as a Shapely (multi)polygon in NZTM coordinates, 
     centroid of polygon as a Shapely point in NZTM coordinates))
    for all polygons in the collection.  
    """
    pc_by_name = {}
    for feature in collection['features']:
        name = feature['properties'][name_field]
        # Get centroid in NZTM coordinates
        if feature['geometry']['type'] == 'Polygon':
            coords = feature['geometry']['coordinates']
            polygon = coords_to_polygon(coords, pj_nztm)
        elif feature['geometry']['type'] == 'MultiPolygon':
            big_coords = feature['geometry']['coordinates']
            polygons = [coords_to_polygon(coords, pj_nztm)
              for coords in big_coords]
            polygon = unary_union(polygons)
        else:
            print('Skipping this problematic feature of type', 
              feature['geometry']['type'])
            continue
        pc_by_name[name] = (polygon, polygon.centroid)
    return pc_by_name

def create_centroids(region=None, name_field='AU2013_NAM', digits=5):
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
    if region is not None:
        prefix = 'data/%s/' % region
    else:
        prefix = 'data/'

    collection = load_json(prefix + 'au_shapes.geojson')
    pc_by_name = get_polygon_and_centroid_by_au_name(collection, 
      name_field=name_field)
    
    # Create CSV and GeoJSON
    features = []
    with open(prefix + 'au_centroids.csv', 'w') as f:
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
    geojson = features_to_feature_collection(features)
    dump_json(geojson, prefix + 'au_centroids.geojson')

def add_fare_zones(region=None):
    """
    Add a fare zone column to the centroids CSV file of the given region.
    Currently, only ``region == 'auckland'`` is implemented.
    """
    assert region == 'auckland',\
      "Only 'region' == 'auckland' is implemented"

    prefix = 'data/%s/' % region

    # Read in fare zones and convert to Shapely polygons
    fare_zones = load_json(prefix + 'monthly_pass_fare_zones.geojson')
    polygon_by_zone = {}
    for feature in fare_zones['features']:
        zone = feature['properties']['fare_zone']
        poly = coords_to_polygon(feature['geometry']['coordinates'])
        old_poly = polygon_by_zone.get(zone, Polygon())
        poly = unary_union([old_poly, poly])
        polygon_by_zone[zone] = poly

    # Read in each centroid and find the fare zone containing it
    new_rows = []
    with open(prefix + 'au_centroids.csv', 'rb') as f:
        reader = csv.reader(f)
        header = reader.next()[:3]
        header.append('fare zone')
        new_rows.append(header)
        for row in reader:            
            # Find the fare zone containing the point
            name, lon, lat = row[:3]
            point = Point(float(row[1]), float(row[2]))
            zone = None
            for z, poly in polygon_by_zone.iteritems():
                if poly.intersects(point):
                    zone = z
                    break
            new_rows.append([name, lon, lat, zone])
    
    # Write new centroids file with fare zone column
    with open(prefix + 'au_centroids.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

def get_sample_points(polygon, n):
    """
    Return ``n`` Shapely points chosen uniformly at random from the 
    given Shapely polygon object.
    """
    from random import uniform

    minx, miny, maxx, maxy = polygon.bounds
    # Sample uniformly at random from the polygon's bounding box
    # and discard points that aren't in the polygon.
    sample_points = []
    i = 0
    while i < n:
        x = uniform(minx, maxx)
        y = uniform(miny, maxy)
        p = Point(x, y)
        if p.intersects(polygon):
            sample_points.append(p)
            i += 1
    return sample_points

def create_sample_points(region, name_field='AU2013_NAM', n=100, digits=5):
    """
    Create a CSV file containing ``n`` random sample points from each area unit
    in a given region in ``REGIONS``.
    Use ``get_sample_points()``).

    For the CSV file create a header row and data rows with the following
    columns:

    1. area unit name
    2. WGS84 longitude of a sample point in the area unit
    3. WGS84 latitude of sample point

    These sample points can then be used to calculate a commute distance
    and time from an area unit to itself.
    For example, for each area unit and each mode of travel one could 
    take the medians of the distances and times from the sample points 
    to the centroid as the representative commute distance and time.

    All longitude and latitude entries are rounded to ``digits``
    decimal places.
    Note that 5 decimal places in longitude and latitude degrees gives
    a precision on the ground of about 1 meter; see
    `here <https://en.wikipedia.org/wiki/Decimal_degrees>`_ . 
    """
    prefix = 'data/%s/' % region
    collection = load_json(prefix + 'au_shapes.geojson')
    pc_by_name = get_polygon_and_centroid_by_au_name(collection, 
      name_field=name_field)
    
    # Create CSV version
    with open(prefix + 'au_sample_points.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['2013 area unit name', 
          'WGS84 longitude of a sample point in the area unit',
          'WGS84 latitude of sample point'])
        for name, pc in sorted(pc_by_name.items()):
            sample_points = get_sample_points(pc[0], n)
            for p in sample_points:
                pp = my_round(pj_nztm(*point_to_tuple(p), inverse=True),
                  digits=digits)
                writer.writerow([name, pp[0], pp[1]])

# Distance and time data functions
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

def median(s):
    """
    Return the median of the given list of numbers.
    """
    if not s:
        return None
    s = list(s)
    s.sort()
    n = len(s)
    if n % 2 == 1:
        return s[n//2]
    else:
        return (s[n//2] + s[n//2 - 1])/2.0

def create_fake_commute_costs(region, name_field='AU2013_NAM',
  n=100):
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
    prefix = 'data/%s/' % region

    collection = load_json(prefix + 'au_shapes.geojson')
    pc_by_name = get_polygon_and_centroid_by_au_name(collection, name_field)
    names = pc_by_name.keys()
    centroids_wgs84 = [pj_nztm(*point_to_tuple(pc[1]), inverse=True)
      for pc in pc_by_name.itervalues()]
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
                distances, times = zip(*[get_bird_distance_and_time(point, a)
                  for point in sample_points])
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

def create_commute_costs(region):
    """
    Take the data in the commute CSV files for this region and 
    convert it into one JSON master file of daily commute cost and time. 
    More specifically, write to ``data/<region>/commute_costs.json`` 
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
    """
    prefix = 'data/%s/' % region

    # Get AU names
    names = []
    with open(prefix + 'au_names.csv') as f:
        reader = csv.reader(f)
        # Skip header
        reader.next()
        for row in reader:
            names.append(row[0])
    names.sort()
    index_by_name = {name: i for (i, name) in enumerate(names)}
    n = len(names)

    # Initialize matrix
    M = {mode: [[(None, None) for j in range(n)] for i in range(n)] 
      for mode in MODES}

    # Assign distance and time values from CSVs
    for mode in MODES:
        filename = prefix + mode + '_commutes.csv'
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            # Skip header row
            reader.next() 
            for row in reader:
                o_name, d_name, distance, time = row
                if (o_name not in index_by_name) or\
                  (d_name not in index_by_name):
                    continue
                if distance:
                    distance = float(distance)
                else:
                    distance = None
                if time:
                    time = float(time)
                else:
                    time = None
                # Save to matrix
                M[mode][index_by_name[o_name]][index_by_name[d_name]] =\
                  (distance, time)

    # Create a cost lower-triangular half-matrix from M
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
    dump_json(data, prefix + 'commute_costs.json')

def improve_auckland_transit_commute_costs():
    """
    Assume ``commute_costs.json`` has been created for the Auckland region
    and improve its transit mode cost estimates by using monthly pass fares.
    """
    prefix = 'data/auckland/'

    # Load original commute costs
    cc = load_json(prefix + 'commute_costs.json')
    M = cc['matrix']
    index_by_name = cc['index_by_name']
    name_by_index = {index_by_name[name]: name for name in index_by_name}

    # Get fare zone by AU name
    zone_by_name = {}
    with open(prefix + 'au_centroids.csv') as f:
        reader = csv.reader(f)
        # Skip header
        reader.next()
        for row in reader:
            name, lon, lat, zone = row
            if zone == '':
                zone = None
            zone_by_name[name] = zone

    # Get one-way daily cost by origin zone and destination zone
    cost_by_od = {}
    with open(prefix + 'monthly_pass_fares.csv') as f:
        reader = csv.reader(f)
        # Skip header
        reader.next()
        for row in reader:
            origin, destination, monthly_cost = row
            if monthly_cost != '':
                daily_cost = float(monthly_cost)/(365/12)
            else:
                daily_cost = None
            cost_by_od[(origin, destination)] = daily_cost

    # Update M['transit'] cost (but not time)
    n = len(M['transit'])
    for i in range(n):
        i_zone = zone_by_name[name_by_index[i]]
        for j in range(i + 1):
            j_zone = zone_by_name[name_by_index[j]] 
            # Update roundtrip daily cost if the original cost is not None or 0
            try:
                cost = round(cost_by_od[(i_zone, j_zone)] +\
                    cost_by_od[(j_zone, i_zone)], 2)
            except (KeyError, TypeError):
                cost = None
            if cost is not None and M['transit'][i][j][0] not in [None, 0]:
                M['transit'][i][j][0] = cost 

    # Write to file
    data = {'index_by_name': index_by_name, 'matrix': M}
    dump_json(data, prefix + 'commute_costs.json')
       
# TODO: delete this function when no longer necessary
def reformat_commutes(filename):
    """
    Given a CSV of commutes with distances in meters and times in minutes,
    convert them to kilometers and hours, respectively.
    Save to new CSV file.
    """ 
    # Assign distance and time values from CSVs
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        M = list(reader)
    filename = filename + '.new'
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['origin area unit', 'destination area unit',
          'distance (kilometers)', 'time (hours)'])
        for row in sorted(M[1:]):
            o_name, d_name, distance, time = row
            # Convert distance to km and time to h 
            if distance:
                distance = round(float(distance)/1000, 3)
            else:
                distance = None
            if time:
                time = round(float(time)/60, 3)
            else:
                time = None
            writer.writerow([o_name, d_name, distance, time])

if __name__ == '__main__':
    region = 'auckland'
    # print('Creating files for %s...' % region)
    # print('  Shapes...')
    # create_shapes(region)
    # print('  Rents...')
    # create_rents(region)
    # print('  Centroids...')
    # create_centroids(region)
    # print('  Sample points...')
    # create_sample_points(region)
    # print('  Fake commute costs...')
    # create_fake_commute_costs(region)
    # print('  Commute costs...')
    # create_commute_costs(region)
    if region == 'auckland':
        add_fare_zones(region)
        improve_auckland_transit_commute_costs()