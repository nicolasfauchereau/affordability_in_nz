# Create a JSON file that contains a matrix of travel distance and
# and travel time estimates between the centroids of 2013 census area units 
# (AUs). 
# Store the matrix in a nested JSON dict of the form
# AU name -> AU name -> (distance in meters, time in seconds)
from __future__ import print_function, division
import datetime as dt 
import json

import pyproj, shapely

INFILE = 'data/Auckland_AUs_2013.geojson'
OUTFILE = 'data/distance_and_time_matrix.json'
NUM_SAMPLE_POINTS = 100

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

# TODO: Update this function
def get_bird_distance_and_time(a, b):
    """
    Given a list of pairs WGS84 longitude-latitude points ``a`` and ``b``, 
    return the distance and time of the quickest path from  ``a`` to ``b``
    in the Open Street Map network. 
    Use `OSRM <http://map.project-osrm.org/>`_.
    """
    d = distance(a[0], a[1], b[0], b[1])
    return my_round((d, d/40), 2)

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
    s.sort()
    n = len(s)
    if n % 2 == 1:
        return s[n//2]
    else:
        return (s[n//2] + s[n//2 - 1])/2.0

def get_polygon_and_centroid_by_name(filename, name_field):
    """
    Assume ``filename`` is the name of a GeoJSON file comprising a feature
    collection of (multi)polygons in WGS84 coordinates, each of which has a 
    name specified in ``feature['properties']['name_field']``. 
    Return a dictionary with the key-value pairs (polygon name, 
    (polygon as a Shapely (multi)polygon in NZTM coordinates, 
     centroid of polygon as a Shapely point))
    for all polygons in the collection.  
    """
    from shapely.geometry import Polygon, MultiPolygon
    from shapely.ops import unary_union

    pc_by_name = {}
    with open(filename, 'rb') as geojson_file:
        collection = json.loads(geojson_file.read())
        for feature in collection['features']:
            name = feature['properties'][name_field]
            # Get centroid in NZTM coordinates
            if feature['geometry']['type'] == 'Polygon':
                coords = feature['geometry']['coordinates'][0]
                coords = [wgs84_to_nztm(*c) for c in coords]
                polygon = Polygon(coords)
            elif feature['geometry']['type'] == 'MultiPolygon':
                polygons = [Polygon([wgs84_to_nztm(*c) for c in coords]) 
                  for coords in feature['geometry']['coordinates'][0]]
                polygon = unary_union(polygons)
            else:
                print('Skipping this problematic feature of type', 
                  feature['geometry']['type'])
                continue
            pc_by_name[name] = (polygon, polygon.centroid)
        return pc_by_name
     
def get_distance_and_time_matrix(filename, name_field, n=NUM_SAMPLE_POINTS):
    """
    Assume ``filename`` is the name of a GeoJSON file comprising a feature
    collection of (multi)polygons in WGS84 coordinates, each of which has a 
    name specified in ``feature['properties']['name_field']``. 
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

    modes = {'walk', 'bicycle', 'car', 'bus'}
    pc_by_name = get_polygon_and_centroid_by_name(filename=filename, 
      name_field=name_field)
    names = pc_by_name.keys()
    N = len(names)
    centroids_wgs84 = [wgs84_to_nztm(*point_to_tuple(pc[1]), inverse=True)
      for pc in pc_by_name.values()]
    index_by_name = {name: i for (i, name) in enumerate(names)}
    M = {m: [] for m in modes}

    # Calculate M
    for i in range(N):
        a = centroids_wgs84[i]
        # Create matrix row M[mode]_i
        for m in modes:
            M[m].append([])
        for j in range(N):
            if j != i:
                b = centroids_wgs84[j] 
                distance, time = get_bird_distance_and_time(a, b)
            else:
                # Get sample points in polyon
                polygon = pc_by_name[names[i]][0]
                sample_points = [wgs84_to_nztm(*point_to_tuple(point), 
                  inverse=True) for point in get_sample_points(polygon, n=n)]
                distances, times = zip(*[get_bird_distance_and_time(point, a)
                  for point in sample_points])
                distance, time = (median(list(distances)), median(list(times)))
            # Create matrix entry M[mode]_ij
            M['walk'][i].append((distance, time*15))
            M['bicycle'][i].append((distance, time*4))
            M['car'][i].append((distance, time))
            M['bus'][i].append((distance, time))

    return index_by_name, M


if __name__ == '__main__':
    # Dump to distance_matrix to JSON
    t1 = dt.datetime.now()
    print(t1, 'Computing...')

    index_by_name, M = get_distance_and_time_matrix(INFILE, 'AU_NAME')
    with open(OUTFILE, 'w') as json_file:
        json.dump({'index_by_name': index_by_name, 'matrix': M}, json_file)
    t2 = dt.datetime.now()
    minutes = (t2 - t1).seconds/60
    print(t2, 'Done. Time elapsed is {:.1f} min.'.format(minutes))