Affordability Maps
***************************
Web maps of affordability in various NZ cities.
Focused on rent, commute, parking, and car ownership costs relative to income.

Requirements
============
- Python >= 2.7
- `RapydScript <https://bitbucket.org/pyjeon/rapydscript>`_ for compiling RapydScript (.pyj) files to JavaScript
- `RapydCSS <https://bitbucket.org/pyjeon/rapydcss>`_ for compiling RapydCSS (.sass) files to CSS

Notes
========
- Inspired in part by the article "Housing and transport expenditure: Socio-spatial indicators of affordability in Auckland" by K. Mattingly and J. Morrissey `[MaMo2014] <http://www.sciencedirect.com/science/article/pii/S0264275114000134>`_ (pay-walled).
- Compare to `the Financial Times London rent map <http://www.ft.com/cms/s/2/ad4ef6a4-503d-11e3-befe-00144feabdc0.html>`_; `this NZ Herald map <http://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=10881119>`_
- Create geojson graphically at `geojson.io <http://geojson.io>`_
- Validate geojson files at `geojsonlint.com <http://geojsonlint.com/>`_
- I got the Auckland 2013 census area units shape file from NZ Stats `here <http://www.stats.govt.nz/browse_for_stats/people_and_communities/Geographic-areas/digital-boundary-files.aspx>`_, simplified and shrunk the shape file (to 5%) with `Mapshaper <http://mapshaper.org/>`_, converted it to GeoJSON with ``ogr2ogr -f geoJSON AU_TA_Auckland_CC.geojson AU_TA_Auckland_CC.shp -t_srs EPSG:4326``, deleted extraneous polygons with `geojson.io <http://geojson.io/#map=12/-36.8964/174.8318>`_

Authors
========
- Alex Raichev