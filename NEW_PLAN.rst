Create an Auckland affordability web map.
A one-time 2013 census snapshot, or maybe a self-updating map.

User Inputs
------------
- Income slider with key marks
- #Bedrooms select
- Workplace marker
- Mode of transport to work select
- Daily parking cost slider with key marks

Outputs
--------
- Web map
- AUs (area units) color coded by total cost as percentage of income
- Legend
- Popup/info box with
    * AU name
    * Rent cost per week per bedroom (absolute cost and fraction of income)
    * Transport to work cost per week
    * Transport to work time estimate 
    * Parking at work cost per week
    * Total cost

Data Sources
-------------
- 2013 census AUs
- 2013 census rent data or Ministry of Business, Innovation, and Employment (MBIE) rent data interpolated
- AU centroid locations
- Shortest distance and travel time matrix between every pair of AUs
- Cost per km per transport mode