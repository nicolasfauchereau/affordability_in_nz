# Some utility functions
from __future__ import print_function, division
import datetime as dt 
import json, csv

import pyproj, shapely

MASTER_SHAPES_FILE = 'data/au_shapes_simplified.geojson'
MASTER_RENTS_FILE = 'data/au_rents.csv'
REGIONS = {'auckland', 'wellington'}
MODES = ['walk', 'bicycle', 'transit', 'car']

def get_au_names(filename, header=True):
    """
    Given a CSV file with initial columns
    
    1. area unit code 
    2. area unit name,

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
            au_names.add(row[1])
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

def create_geojson(region, name_field='AU2013_NAM'):
    """
    Create the GeoJSON file for a given region from ``REGIONS``.
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
    print('Got shapes for each AU?', success)
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
    print('Got rents for each AU?', success)
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
    from shapely.geometry import Polygon
    from shapely.geometry.polygon import LinearRing

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
    from shapely.geometry import Polygon, MultiPolygon
    from shapely.ops import unary_union

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

def create_centroids(region, name_field='AU2013_NAM'):
    """
    Create a GeoJSON and CSV file containing the centroids of the area
    units for a given region from ``REGIONS``.

    For the CSV file create a header row and data rows with the following
    columns:

    1. area unit name
    2. WGS84 longitude of area unit
    3. WGS84 latitude of area unit.

    For the GeoJSON file, create feature collection of point features,
    one for each centroid.
    """
    prefix = 'data/%s/' % region

    collection = load_json(prefix + 'au_shapes.geojson')
    pc_by_name = get_polygon_and_centroid_by_au_name(collection, 
      name_field=name_field)
    
    # Create CSV version
    with open(prefix + 'au_centroids.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['2013 area unit name', 
          'WGS84 longitude of centroid of area unit',
          'WGS84 latitude of centroid of area unit'])
        for name, pc in pc_by_name.items():
            centroid = pj_nztm(*point_to_tuple(pc[1]), inverse=True)
            writer.writerow([name, centroid[0], centroid[1]])

    # Create GeoJSON version
    features = []
    for name, pc in pc_by_name.items():
        # Get centroid in WGS84 coords
        centroid = pj_nztm(*point_to_tuple(pc[1]), inverse=True)
        # Create GeoJSON point feature

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

    geojson = features_to_feature_collection(features)
    dump_json(geojson, prefix + 'au_centroids.geojson')

def get_sample_points(polygon, n):
    """
    Return ``n`` Shapely points chosen uniformly at random from the 
    given Shapely polygon object.
    """
    from shapely.geometry import Point
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

def create_sample_points(region, name_field='AU2013_NAM', n=100):
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
        for name, pc in pc_by_name.items():
            sample_points = get_sample_points(pc[0], n)
            for p in sample_points:
                pp = my_round(pj_nztm(*point_to_tuple(p), inverse=True))
                writer.writerow([name, pp[0], pp[1]])

# Distance and time data functions
def distance(lon1, lat1, lon2, lat2):
    """
    Given two (longitude, latitude) points in degrees, 
    compute their great circle distance in km on a spherical Earth of 
    radius 6137 km.  
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
    return the distance and time of the quickest path from  ``a`` to ``b``
    as the bird flies (at 40 kph).
    """
    d = distance(a[0], a[1], b[0], b[1])
    return my_round((d, d/40), 2)

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

def create_fake_commutes(region, name_field='AU2013_NAM',
  n=100):
    """
    Given a region in ``REGIONS``, get the regions decoded GeoJSON 
    feature collection of (multi)polygons in WGS84 coordinates, 
    each of which has a name specified in 
    ``feature['properties']['name_field']``, and return the output pair 
    ``(index_by_name, M)``, where ``M`` is a nested
    dictionary/matrix such that ``M[mode][i][j]`` equals a fake distance in km
    and a fake time in hours that it takes to travel from the centroid of 
    polygon with index ``i >= 0`` to the centroid of polygon with index 
    ``j >= 0``.
    The distance used ('walk', 'bicycle', 'car', 'transit') = (d, d, d, d)
    and the time used is (t*15, t*4, t, t), where d and t come from
    ``get_bird_distance_and_time()``
    The dictionary ``index_by_name`` maps polygon names to their indices. 
    ``M[i][i]`` is obtained by choosing ``n`` points uniformly at random 
    from polygon ``i`` and taking the median of the distances and times 
    from each of these points to the polygon's centroid.
    """
    prefix = 'data/%s/' % region

    collection = load_json(prefix + 'au_shapes.geojson')
    pc_by_name = get_polygon_and_centroid_by_au_name(collection, name_field)
    names = pc_by_name.keys()
    N = len(names)
    centroids_wgs84 = [pj_nztm(*point_to_tuple(pc[1]), inverse=True)
      for pc in pc_by_name.values()]
    index_by_name = {name: i for (i, name) in enumerate(names)}
    M = {m: [] for m in MODES}

    # Calculate M
    for i in range(N):
        a = centroids_wgs84[i]
        # Create matrix row M[mode]_i
        for m in MODES:
            M[m].append([])
        for j in range(N):
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
            # Create matrix entry M[mode]_ij
            M['walk'][i].append((distance, time*15))
            M['bicycle'][i].append((distance, time*4))
            M['car'][i].append((distance, time))
            M['transit'][i].append((distance, time))

    data = {'index_by_name': index_by_name, 'matrix': M}
    dump_json(data, prefix + 'fake_commutes.json')

# TODO: Clean up the functions below.
# Miscellaneous commute data functions in various states of disarray.
def create_commutes(collection, name_field):
    """
    Given a decoded GeoJSON feature collection of (multi)polygons in WGS84
    coordinates, each of which has a name specified in 
    ``feature['properties']['name_field']``, return the output pair 
    ``(index_by_name, M)``, where ``M`` is a nested
    dictionary/matrix such that ``M[mode][i][j]`` equals the distance in km
    and the time in hours that it takes to travel from centroid of 
    polygon with index ``i >= 0`` to the centroid of polygon with index 
    ``j >= 0`` through the Open Street Map road network by the mode of
    transport ``mode``, which is one of 'walk', 'bicycle', 'car', 'transit'.
    The dictionary ``index_by_name`` gives maps polygon names to their
    indices. 
    ``M[i][i]`` is obtained by choosing ``n`` points uniformly at random 
    from polygon ``i`` and taking the median of the distances and times 
    from each of these points to the polygon's centroid.

    Get data from CSVs.
    """
    prefix = 'data/%s/' % region

    pc_by_name = get_polygon_and_centroid_by_au_name(collection, name_field)
    names = pc_by_name.keys()
    N = len(names)
    index_by_name = {name: i for (i, name) in enumerate(names)}
    M = {mode: {} for mode in MODES}

    # Read distance and time data from CSVs
    for mode in MODES:
        filename = prefix + mode + '_commutes.csv'
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            # Skip header row
            reader.next() 
            for row in reader:
                origin_name, destination_name, distance, time = row
                # Convert distance to km and time to h 
                if distance:
                    distance = round(float(distance)/1000, 1)
                elif mode == 'transit':
                    # Until get distance data for public transport,
                    # used car distance
                    try:
                        distance = M['car'][origin_name][destination_name][0]
                    except KeyError:
                        distance = None
                else:
                    distance = None
                time = round(float(time)/60, 1)
                # Save to matrix
                if origin_name not in M[mode]:
                    M[mode][origin_name] =\
                      {destination_name: (distance, time)}
                else:
                    M[mode][origin_name][destination_name] =\
                      (distance, time) 

    # Compress each M[mode] by turning it into a list of lists.
    MM = {mode: [] for mode in MODES}
    for mode in MODES:
        for on  in origin_names:
            row = []
            for dn in origin_names:
                try:
                    row.append(M[mode][on][dn])
                except KeyError:
                    row.append((None, None)) 
            MM[mode].append(row)    
    index_by_name = {on: i for (i, on) in enumerate(origin_names)}
    return index_by_name, MM

# TODO: finish this function
def get_distance_and_time_diagonal(collection):
    pc_by_name = get_polygon_and_centroid_by_au_name(collection, 'AU_NAME')
    for au_name, pc in pc_by_name.items():
        for mode in MODES:
            get_distance_and_time_to_self(pc[0], pc[1], mode=mode)
        
def get_distance_and_time_to_self(polygon, centroid, n=100,
  mode=MODES[0]):
    """
    Given a polygon and its centroid in NZTM coordinates,
    return...
    """
    centroid = pj_nztm(*point_to_tuple(centroid), inverse=True)
    sample_points = get_sample_points(polygon, n)
    sample_points = [pj_nztm(*point_to_tuple(p), inverse=True) 
      for p in sample_points]
    distances, times = zip(*[get_mapquest_distance_and_time(centroid, p, mode) 
        for p in sample_points])
    return(median(distances), median(times))

def get_mapquest_distance_and_time(a, b, mode='car'):
    """
    Given WGS84 longitude-latitude points ``a`` and ``b``,
    return the distance in kilometers and the time in minutes of the 
    quickest path from ``a`` to ``b`` in the Mapquest road network for 
    the specified mode of transit; mode options are 'walk', 'bicycle', 
    'car', and 'transit'.
    Computed with the `Mapquest API <http://www.mapquestapi.com/directions/#advancedrouting>`_.
    """
    import urllib2

    if mode == 'walk':
        mode = 'pedestrian'
    elif mode == 'bicycle':
        pass
    elif mode == 'transit':
        mode = 'multimodal'
    else:
        mode = 'fastest'

    url = 'http://www.mapquestapi.com/directions/v2/route?key=Fmjtd|luur2l622u%2C2n%3Do5-90ya0y&from='
    url += '{!s},{!s}&to={!s},{!s}'.format(a[1], a[0], b[1], b[0])
    url += '&routeType=' + mode
    url += '&unit=k&doReverseGeocode=false&narrativeType=none'
    # Send query and retrieve data
    result = json.load(urllib2.urlopen(url))
    return result['route']['distance'], result['route']['time']/60

# TODO: return better formatted outputs
def get_google_distance_and_time(a, b, mode='car', many_to_one=False,
  use_tor=True):
    """
    Given WGS84 longitude-latitude points ``a`` and ``b``,
    return the distance in kilometers and the time in minutes of the 
    quickest path from ``a`` to ``b`` in the Mapquest road network for 
    the specified mode of transit; mode options are 'walk', 'bicycle', 
    'car', and 'transit'.
    Computed with the `Google API <>`_.
    If ``use_tor == True``, then perform API calls through Tor,
    assuming you have it running.
    """
    import urllib2

    if use_tor:
        # Connect to the internet through Tor
        import socks
        from socketshandler import SocksiPyHandler

        opener = urllib2.build_opener(SocksiPyHandler(
          socks.PROXY_TYPE_SOCKS5, "localhost", 9150))
        open_sesame = opener.open
        # Test
        print('IP address', open_sesame('https://httpbin.org/ip').read())
    else:
        open_sesame = urllib2.urlopen

    if mode == 'walk':
        mode = 'walking'
    elif mode == 'bicycle':
        mode = 'bicycling'
    elif mode == 'transit':
        # 19:30 12 Mar 2014 GMT = 8:30 13 Mar 2014 Auckland time
        # See http://www.onlineconversion.com/unix_time.htm
        mode = 'transit&arrival_time=1394652600' 
    else:
        mode = 'driving'

    url = 'http://maps.googleapis.com/maps/api/directions/json?origin='
    url += '{!s},{!s}&destination={!s},{!s}'.format(a[1], a[0], b[1], b[0])
    url += '&mode=' + mode + '&sensor=false'
    # Send query and retrieve data
    result = json.load(open_sesame(url))
    return result

# TODO: return better formatted outputs
def get_google_distance_matrix(origins, destinations, mode='driving',
  use_tor=True):
    """
    Given a list of origins as WGS84 longitude-latitude pairs,
    a list of destinations of the same length and form,
    and a mode of transport ('driving', 'bicycling', or 'walking'), 
    return the origin-destination matrix computed by Google Maps API; see
    `here <https://developers.google.com/maps/documentation/distancematrix/>`_.

    The output matrix ``M``, is in decoded JSON form, where
    ``M['rows'][i]['elements'][j]`` contains time and distance estimates 
    for the trip from ``origins[i]`` to ``destinations[j]`` in the form of 
    a dictionary ``v``, where ``v['distance']['value']`` is the travel
    distance in meters and ``v['duration']['value']`` is the travel time in 
    seconds.

    If ``use_tor == True``, then perform API calls through Tor,
    assuming you have it running.
    """
    import urllib2

    if use_tor:
        # Connect to the internet through Tor
        import socks
        from socketshandler import SocksiPyHandler

        opener = urllib2.build_opener(SocksiPyHandler(
          socks.PROXY_TYPE_SOCKS5, "localhost", 9150))
        open_sesame = opener.open
        # Test
        print('IP address', open_sesame('https://httpbin.org/ip').read())
    else:
        open_sesame = urllib2.urlopen

    # Create query url
    url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins='
    for (lon, lat) in origins:
        url += '{:.5f},{:.5f}|'.format(lat, lon)
    # Remove trailing '|'
    url = url[:-1]
    url += '&destinations='
    for (lon, lat) in destinations:
        url += '{:.5f},{:.5f}|'.format(lat, lon)
    url = url[:-1]
    url += '&mode=' + mode + '&sensor=false'

    print('url=', url)
    # Send query and retrieve data
    return json.load(open_sesame(url))

def test_api(use_tor=True):
    a = [174.7103025602929,-36.77207046318112]
    b = [174.70080752730942,-36.914615337299345]
    g1 = get_google_distance_and_time(a, b, use_tor=use_tor)
    g2 = get_google_distance_matrix([a, b], [a, b], use_tor=use_tor)
    print()
    print(g1)
    print('-'*40)
    print(g2)

if __name__ == '__main__':
    region = 'wellington'
    print('Creating files for %s...' % region)
    create_geojson(region)
    create_rents(region)
    create_centroids(region)
    create_sample_points(region)
    create_fake_commutes(region)
    # test_api(use_tor=True)