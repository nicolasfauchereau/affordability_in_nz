Affordability in New Zealand 
********************************
Web maps of affordability for various New Zealand (NZ) cities.
Focused on rent, commute, parking, and car ownership costs relative to income.
Live site coming soon...

Requirements
============
- Python >= 2.7
- `RapydScript <https://bitbucket.org/pyjeon/rapydscript>`_ for compiling RapydScript (.pyj) files to JavaScript
- `RapydCSS <https://bitbucket.org/pyjeon/rapydcss>`_ for compiling RapydCSS (.sass) files to CSS

Instructions
=============
- To view the Auckland map locally run ``python -m SimpleHTTPServer 8001`` in your cloned version of this repository and point your browser to ``localhost:8001/auckland``.
- By the way, for auto-compiling RapydScript files, `this Gist <https://gist.github.com/araichev/8923682>`_ can be handy.

Notes
========
- This project is inspired in part by the article "Housing and transport expenditure: Socio-spatial indicators of affordability in Auckland" by K. Mattingly and J. Morrissey `[MaMo2014] <http://www.sciencedirect.com/science/article/pii/S0264275114000134>`_ (pay-walled) and is funded in part by `MRCagney <http://www.mrcagney.com>`_.
- Shape files for all NZ 2013 census area units are available from Statistics New Zealand from `here <http://www.stats.govt.nz/browse_for_stats/people_and_communities/Geographic-areas/digital-boundary-files.aspx>`_.  You can use them and `Mapshaper <http://www.mapshaper.org/>`_ to create GeoJSON polygons for web maps.
- The 2013 census rent data in ``nz_census_rent_data_2013.xlsx`` comes from Statistics New Zealand as a custom data request and is licensed under the Creative Commons Attribution 3.0 New Zealand license.

Authors
========
- Saeid Adli
- Alex Raichev