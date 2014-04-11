Affordability in New Zealand 
********************************
Web maps of affordability for various New Zealand (NZ) cities.
Focused on rent, commute, parking, and car ownership costs relative to income.

Thanks heaps to the `MRCagney <http://www.mrcagney.co.nz>`_ for donating to this projet!

Requirements
============
- `RapydML <https://bitbucket.org/pyjeon/rapydml>`_ for compiling RapydML (.pyml) files to HTML
- `RapydCSS <https://bitbucket.org/pyjeon/rapydcss>`_ for compiling RapydCSS (.sass) files to CSS
- `RapydScript <https://bitbucket.org/pyjeon/rapydscript>`_ for compiling RapydScript (.pyj) files to JavaScript
- Python >= 2.7 for data processing in ``utils.py``
- `Shapely <http://toblerity.org/shapely/>`_ for geodata processing in ``utils.py``

Instructions
=============
- To view the Auckland map locally, run ``python -m SimpleHTTPServer 8001`` in your cloned version of this repository and point your browser to ``localhost:8001``.
- For auto-compiling RapydScript files, `this Gist <https://gist.github.com/araichev/8923682>`_ is useful.

Notes
======
- This project is inspired in part by the article "Housing and transport expenditure: Socio-spatial indicators of affordability in Auckland" by K. Mattingly and J. Morrissey `[MaMo2014] <http://www.sciencedirect.com/science/article/pii/S0264275114000134>`_ (pay-walled).
- The shape file containing all NZ 2013 census area units comes from Statistics New Zealand (Stats NZ) from `here <http://www.stats.govt.nz/browse_for_stats/people_and_communities/Geographic-areas/digital-boundary-files.aspx>`_.  It was converted to GeoJSON with GDAL via the command ``ogr2ogr -f geoJSON -t_srs EPSG:4326 <name>.geojson <name>.shp``.  See `this page <http://ben.balter.com/2013/06/26/how-to-convert-shapefiles-to-geojson-for-use-on-github/>`_ for more details. The resulting GeoJSON file was then simplified down to 15% with `Mapshaper <http://www.mapshaper.org/>`_ to use for the web maps.
- The median gross annual incomes of employed Aucklanders, Wellingtonians, etc. come from Statistics New Zealand from the June 2013 income survey `here <http://www.stats.govt.nz/browse_for_stats/income-and-work/Income/nz-income-survey-info-releases.aspx>`_. 
- The 2013 census rent data comes from Stats NZ from a custom data request and is licensed under the Creative Commons Attribution 3.0 New Zealand license.
- Distances and times between area unit centroids are calculated through the street network for walking, bicycling, and driving modes using ArcGIS. Transit distances and times are calculated using the Google Maps API for 13 March 2013 around 08:30. 
- 2013 area unit names and codes by region come from Stats NZ from the following links. I exclude water area units.
    - `Auckland <http://www.stats.govt.nz/Census/2013-census/data-tables/population-dwelling-tables/auckland.aspx>`_
    - `Canterbury <http://www.stats.govt.nz/Census/2013-census/data-tables/population-dwelling-tables/canterbury.aspx>`_ 
    - `Wellington <http://www.stats.govt.nz/Census/2013-census/data-tables/population-dwelling-tables/wellington.aspx>`_
    - `Waikato <http://www.stats.govt.nz/Census/2013-census/data-tables/population-dwelling-tables/waikato.aspx>`_
- Auckland transit distances are car distances for now. Still running the Google Maps queries.

Resources
============
- `GeoJSONLint <http://geojsonlint.com/>`_ for validating and visualizing GeoJSON online.

Todo
====
- Make the app useable by couples by adding and extra map marker and optional questions for the partner's commute and parking costs.
- Replace the zero distance of a centroid to itself with the median distance of N >= 100 points to the centroid, where the points are sampled uniformly at random from the area unit in question.
- Improve transit cost estimates, possibly using fare zones. 
- Improve driving and transit times by factoring in traffic somehow.  

Authors
========
- Saeid Adli
- Alex Raichev