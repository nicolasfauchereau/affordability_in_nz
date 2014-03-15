Affordability in New Zealand 
********************************
Web maps of affordability for various New Zealand (NZ) cities.
Focused on rent, commute, parking, and car ownership costs relative to income.
For example, see the `Auckland demo site <https://rawgithub.com/araichev/affordability_in_nz/master/auckland/index.html>`_.

Requirements
============
- Python >= 2.7
- `RapydScript <https://bitbucket.org/pyjeon/rapydscript>`_ for compiling RapydScript (.pyj) files to JavaScript
- `RapydCSS <https://bitbucket.org/pyjeon/rapydcss>`_ for compiling RapydCSS (.sass) files to CSS

Notes
========
- Inspired in part by the article "Housing and transport expenditure: Socio-spatial indicators of affordability in Auckland" by K. Mattingly and J. Morrissey `[MaMo2014] <http://www.sciencedirect.com/science/article/pii/S0264275114000134>`_ (pay-walled).
- A shape file for all NZ 2013 census area units shape file can be obtained from Statistics New Zealand from `here <http://www.stats.govt.nz/browse_for_stats/people_and_communities/Geographic-areas/digital-boundary-files.aspx>`_.
- The 2013 census rent data in ``nz_census_rent_data_2013.xlsx`` comes from Statistics New Zealand as a custom data request and is licensed under the Creative Commons Attribution 3.0 New Zealand license.

Authors
========
- Saeid Adli
- Alex Raichev