class Region(object):
    """
    Represents a region of New Zealand (NZ).
    """

    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        self.area_units = None
        self.shapes = None
        self.centroids = None
        self.rents = None
        self.walk_commutes = None
        self.bicycle_commutes = None
        self.transit_commutes = None
        self.car_commutes = None
        self.commute_costs = None


