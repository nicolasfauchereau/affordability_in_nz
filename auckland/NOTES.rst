 Notes
 ******
 - The Auckland 2013 area units came from Statistics New Zealand from `here <http://www.stats.govt.nz/browse_for_stats/people_and_communities/Geographic-areas/digital-boundary-files.aspx>`_, were simplified (to 5%) with `Mapshaper <http://mapshaper.org/>`_, and were converted to GeoJSON via ``ogr2ogr -f geoJSON AU_TA_Auckland_CC.geojson AU_TA_Auckland_CC.shp -t_srs EPSG:4326``.
   Etraneous water area units were deleted visually using `geojson.io <http://geojson.io>`_.
- Distances between area unit centroids were calculated through the Auckland street network using ArcGIS. For public transport times, Auckland GTFS feed was used.

Todo
====
- Get public transport data that includes ferry and rail.
- Get a better public transport cost estimate using Hop card zones.
- Replace the zero distance of a centroid to itself with the median distance of N >= 100 points to the centroid, where the points are sampled uniformly at random from the area unit in question.
