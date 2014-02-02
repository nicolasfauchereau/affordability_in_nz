Auckland Rent-Income Ratio map
********************************

Requirements
============
- `RapydScript <https://bitbucket.org/pyjeon/rapydscript>`_ for compiling RapydScript (.pyj) files to JavaScript
- `RapydCSS <https://bitbucket.org/pyjeon/rapydcss>`_ for compiling RapydCSS (.sass) files to CSS

Git Workflow
=============
Let's use `this centralized Git workflow <https://www.atlassian.com/git/workflows#!workflow-centralized>`_.
If our project becomes too complex for that, then we can switch to `this feature branch Git workflow <https://www.atlassian.com/git/workflows#!workflow-feature-branch>`_. 

Notes
========
- Trello board for this project is `here <https://trello.com/b/93UFI6M3/rent-map>`_
- Inspiration comes from `the Financial Times London rent map <http://www.ft.com/cms/s/2/ad4ef6a4-503d-11e3-befe-00144feabdc0.html>`_
- Compare to `this map <http://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=10881119>`_ in the NZ Herald
- Mean rents come from `this NZ government CSV <http://utilities.dbh.govt.nz/userfiles/open-data/mean-rents.csv>`_
- Create geojson graphically at `geojson.io <http://geojson.io>`_
- Validate geojson files at `geojsonlint.com <http://geojsonlint.com/>`_
- Got the Auckland 2013 census area units shape file from `NZ Stats <http://www.stats.govt.nz/browse_for_stats/people_and_communities/Geographic-areas/digital-boundary-files.aspx>`_, simplified and shrunk the shape file with `Mapshaper <http://mapshaper.org/>`_, converted it to GeoJSON with ``ogr2ogr -f geoJSON AU_TA_Auckland_CC.geojson AU_TA_Auckland_CC.shp -t_srs EPSG:4326``, deleted extraneous polygons with `geojson.io <http://geojson.io/#map=12/-36.8964/174.8318>`_