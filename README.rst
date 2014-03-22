Affordability in New Zealand 
********************************
Web maps of affordability for various New Zealand (NZ) cities.
Focused on rent, commute, parking, and car ownership costs relative to income.
Live site coming soon...

Requirements
============
- `RapydML <https://bitbucket.org/pyjeon/rapydml>`_ for compiling RapydML (.pyml) files to HTML
- `RapydCSS <https://bitbucket.org/pyjeon/rapydcss>`_ for compiling RapydCSS (.sass) files to CSS
- `RapydScript <https://bitbucket.org/pyjeon/rapydscript>`_ for compiling RapydScript (.pyj) files to JavaScript
- Python >= 2.7 for data processing

Instructions
=============
- To view the Auckland map locally run ``python -m SimpleHTTPServer 8001`` in your cloned version of this repository and point your browser to ``localhost:8001``.
- By the way, for auto-compiling RapydScript files, `this Gist <https://gist.github.com/araichev/8923682>`_ can be handy.

Notes
======
- This project is inspired in part by the article "Housing and transport expenditure: Socio-spatial indicators of affordability in Auckland" by K. Mattingly and J. Morrissey `[MaMo2014] <http://www.sciencedirect.com/science/article/pii/S0264275114000134>`_ (pay-walled).
- The shape file containing all NZ 2013 census area units comes from Statistics New Zealand (Stats NZ) from `here <http://www.stats.govt.nz/browse_for_stats/people_and_communities/Geographic-areas/digital-boundary-files.aspx>`_.  It was converted to GeoJSON with GDAL via the command ``ogr2ogr -f geoJSON -t_srs EPSG:4326 <name>.geojson <name>.shp``.  See `this page <http://ben.balter.com/2013/06/26/how-to-convert-shapefiles-to-geojson-for-use-on-github/>`_ for more details. The resulting GeoJSON file was then simplified down to 15% with `Mapshaper <http://www.mapshaper.org/>`_ to use for the web map.
- The 2013 census rent data comes from Stats NZ from a custom data request and is licensed under the Creative Commons Attribution 3.0 New Zealand license.
- Thanks heaps to the `MRCagney <http://www.mrcagney.com>`_ Auckland team for donating to this projet!

Notes on Auckland
==================
- Auckland 2013 area unit codes and names come from Stats NZ from `here <http://www.stats.govt.nz/Census/2013-census/data-tables/population-dwelling-tables/auckland.aspx>`_.  Water area units were ignored.
- Distances between area unit centroids were calculated through the Auckland street network using ArcGIS. For public transport times, Auckland's GTFS feed was used.

Notes on Wellington
====================
- Wellington 2013 area unit codes and names come from Stats NZ from `here <http://www.stats.govt.nz/Census/2013-census/data-tables/population-dwelling-tables/wellington.aspx>`_

Todo
====
- Get public transport data that includes ferry and rail.
- Get a better public transport cost estimate using Hop card zones.
- Replace the zero distance of a centroid to itself with the median distance of N >= 100 points to the centroid, where the points are sampled uniformly at random from the area unit in question.

Authors
========
- Saeid Adli
- Alex Raichev