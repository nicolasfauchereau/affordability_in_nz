# Some utility functions
from __future__ import print_function, division
import datetime as dt 
import json, csv

import pyproj, shapely


NUM_SAMPLE_POINTS = 100
MODES = ['walk', 'bicycle', 'public_transport', 'car']

def get_json(filename):
    """
    Decode a JSON file given its name.
    """
    with open(filename, 'rb') as f:
        return json.loads(f.read())

def get_prop_list(collection, prop):
    """
    Given a decoded GeoJSON feature collection, return 
    ``[f['properties'][prop] for f in collection['features']]``
    """
    return [f['properties'][prop] for f in collection['features']]

def get_au_names(collection, name_field='AU_NAME'):
    """
    Given a decoded GeoJSON feature collection of NZ area units, 
    return the names of the area units as a list.
    Assume the name of an area unit ``f`` is ``f['properties'][name_field]``. 
    """
    au_names = get_prop_list(collection, name_field)
    return sorted(au_names)

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

def get_mapquest_distance_and_time(a, b, mode='car'):
    """
    Given WGS84 longitude-latitude points ``a`` and ``b``,
    return the distance in kilometers and the time in minutes of the 
    quickest path from ``a`` to ``b`` in the Mapquest road network for 
    the specified mode of transit; mode options are 'walk', 'bicycle', 
    'car', and 'public_transport'.
    Computed with the `Mapquest API <http://www.mapquestapi.com/directions/#advancedrouting>`_.
    """
    import urllib2

    if mode == 'walk':
        mode = 'pedestrian'
    elif mode == 'bicycle':
        pass
    elif mode == 'public_transport':
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

def get_google_distance_and_time(a, b, mode='car', many_to_one=False):
    """
    Given WGS84 longitude-latitude points ``a`` and ``b``,
    return the distance in kilometers and the time in minutes of the 
    quickest path from ``a`` to ``b`` in the Mapquest road network for 
    the specified mode of transit; mode options are 'walk', 'bicycle', 
    'car', and 'public_transport'.
    Computed with the `Google API <>`_.
    """
    import urllib2

    if mode == 'walk':
        mode = 'walking'
    elif mode == 'bicycle':
        mode = 'bicycling'
    elif mode == 'public_transport':
        # 19:30 12 Mar 2014 GMT = 8:30 13 Mar 2014 Auckland time
        # See http://www.onlineconversion.com/unix_time.htm
        mode = 'transit&arrival_time=1394652600' 
    else:
        mode = 'driving'

    url = 'http://maps.googleapis.com/maps/api/directions/json?origin='
    url += '{!s},{!s}&destination={!s},{!s}'.format(a[1], a[0], b[1], b[0])
    url += '&mode=' + mode + '&sensor=false'
    print('url=', url)
    # Send query and retrieve data
    result = json.load(urllib2.urlopen(url))
    return result

def get_google_distance_matrix(origins, destinations, mode='driving'):
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
    """
    import urllib2

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
    return json.load(urllib2.urlopen(url))

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

def point_to_tuple(p):
    """
    Convert the given Shapely point to an (x, y) tuple.
    """
    return (p.x, p.y)

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
   
def get_polygon_and_centroid_by_name(collection, name_field):
    """
    Given a decoded GeoJSON feature collection of (multi)polygons in 
    WGS84 coordinates, each of which has a 
    name specified in ``feature['properties'][name_field]``. 
    Return a dictionary with the key-value pairs (polygon name, 
    (polygon as a Shapely (multi)polygon in NZTM coordinates, 
     centroid of polygon as a Shapely point))
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

def get_centroids_geojson(collection, name_field):
    """
    Given a decode GeoJSON feature of (multi)polygons in WGS84 coordinates,
    each of which has a name specified in 
    ``feature['properties'][name_field]``, return a decoded GeoJSON feature 
    collection of the polygon centroids as point features.
    """
    pc_by_name = get_polygon_and_centroid_by_name(collection,
      name_field)
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

    geojson = {
      'type': 'FeatureCollection',
      'features': features,
    }
    return geojson

def get_distance_and_time_matrix(origin_names):
    """
    Return the output pair ``(index_by_name, M)``, where ``M`` is a nested
    dictionary/matrix such that ``M[mode][i][j]`` equals the distance in km
    and the time in hours that it takes to travel from centroid of 
    polygon with index ``i >= 0`` to the centroid of polygon with index 
    ``j >= 0`` through the Open Street Map road network by the mode of
    transport ``mode``, which is one of 'walk', 'bicycle', 'car', 'bus'.
    The dictionary ``index_by_name`` gives maps polygon names to their
    indices. 
    ``M[i][i]`` is obtained by choosing ``n`` points uniformly at random 
    from polygon ``i`` and taking the median of the distances and times 
    from each of these points to the polygon's centroid.
    """
    from itertools import product

    M = {mode: {} for mode in MODES}

    # Read distance and time data from CSVs
    for mode in MODES:
        filename = 'data/' + mode + '_distance_and_time.csv'
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            # Skip header row
            reader.next() 
            for row in reader:
                od_pair, distance, time = row
                origin_name, destination_name = od_pair.split(' - ')
                # Convert distance to km and time to h 
                if distance:
                    distance = round(float(distance)/1000, 1)
                elif mode == 'public_transport':
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

def get_distance_and_time_matrix_online(collection, name_field, 
  n=NUM_SAMPLE_POINTS):
    """
    Given a decoded GeoJSON feature collection of (multi)polygons in WGS84
    coordinates, each of which has a name specified in 
    ``feature['properties']['name_field']``, return the output pair 
    ``(index_by_name, M)``, where ``M`` is a nested
    dictionary/matrix such that ``M[mode][i][j]`` equals the distance in km
    and the time in hours that it takes to travel from centroid of 
    polygon with index ``i >= 0`` to the centroid of polygon with index 
    ``j >= 0`` through the Open Street Map road network by the mode of
    transport ``mode``, which is one of 'walk', 'bicycle', 'car', 'bus'.
    The dictionary ``index_by_name`` gives maps polygon names to their
    indices. 
    ``M[i][i]`` is obtained by choosing ``n`` points uniformly at random 
    from polygon ``i`` and taking the median of the distances and times 
    from each of these points to the polygon's centroid.
    """
    from itertools import product

    pc_by_name = get_polygon_and_centroid_by_name(collection, name_field)
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
            M['public_transport'][i].append((distance, time))

    return index_by_name, M

# TODO: finish this function
def get_distance_and_time_diagonal(collection):
    pc_by_name = get_polygon_and_centroid_by_name(collection, 'AU_NAME')
    for au_name, pc in pc_by_name.items():
        for mode in MODES:
            get_distance_and_time_to_self(pc[0], pc[1], mode=mode)
        
def get_distance_and_time_to_self(polygon, centroid, n=NUM_SAMPLE_POINTS,
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

def get_rents(filename, au_names, max_bedrooms=5, header=True):
    """
    Given the name of a CSV file in which each row contains as its first
    several entries
    
        #. area unit name
        #. number of bedrooms in dwelling
        #. count
        #. median weekly rent paid,
    
    return a nested dictionary of median weekly rent paid by number of
    bedrooms by area unit name.
    More specifically, the keys of the dictionary are the strings in 
    ``au_names`` and each corresponding value in a dictionary with
    key-value pair (number of bedrooms, median weekly rent paid for a
    dwelling with that number of bedrooms in the given area unit).
    Only get data for dwellings with at most ``max_bedrooms`` bedrooms.
    If ``header == True``, then skip the first row of the CSV file.
    """
    # Initialize output
    rent_by_num_bedrooms_by_au_name =\
      {au_name: {i: None for i in range(1, max_bedrooms + 1)} 
      for au_name in au_names}
    au_names_set = set(au_names)
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        if header:
            # Skip header row
            reader.next() 
        for row in reader:
            au_name, num_bedrooms, count, rent = row[:4]
            if au_name not in au_names_set or\
              num_bedrooms not in [str(i) for i in range(max_bedrooms + 1)] or\
              not rent:
                # Skip row. 
                # Note that null rents are already recorded in the output.
                continue
            num_bedrooms = int(num_bedrooms)
            rent = int(rent)
            rent_by_num_bedrooms_by_au_name[au_name][num_bedrooms] = rent

    return rent_by_num_bedrooms_by_au_name

def write_rents_to_json(csv_filename, json_filename, au_names, max_bedrooms=5,
  header=True):
    """
    Run ``get_rents(csv_filename, au_names, max_bedrooms, header)``
    and dump the result to a JSON file with the name ``json_filename``.
    """
    rents = get_rents(csv_filename, au_names, max_bedrooms, header)
    with open(json_filename, 'w') as f:
        json.dump(rents, f)

if __name__ == '__main__':
    #collection = get_json('data/Auckland_AUs_2013.geojson')
    #au_names = get_au_names(collection)
    #rents = get_rents('../nz_census_rent_data_2013.csv', au_names)
    #print(rents)
    #print(len(au_names), len(rents))
    # write_rents_to_json('../nz_census_rents_2013.csv', 
    #   'data/auckland_median_rents_2013.json', au_names)
    a = (174.76196765899655, -36.846315278298114)
    b = (174.7931671142578, -36.88250409463316)
    result = get_mapquest_distance_and_time(a, b, 'car')
    print(result)