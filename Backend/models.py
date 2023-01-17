#from app import db


class GasPowerPlant():
    '''__tablename__ = "gas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    fuel_price = db.Column(db.Float, nullable=False)
    co2_emmision = db.Column(db.Float, nullable=False)
    power_max = db.Column(db.Float, nullable=False)
    power_min = db.Column(db.Float, nullable=False)'''

    def __init__(self, id, name, price, emmision, p_min, p_max):
        self.id = id
        self.name = name
        self.fuel_price = price
        self.co2_emmision = emmision
        self.power_max = p_max
        self.power_min = p_min


class CoalPowerPlant():
    '''__tablename__ = "coal"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    fuel_price = db.Column(db.Float, nullable=False)
    co2_emmision = db.Column(db.Float, nullable=False)
    power_max = db.Column(db.Float, nullable=False)
    power_min = db.Column(db.Float, nullable=False)'''

    def __init__(self, id, name, price, emmision, p_min, p_max):
        self.id = id
        self.name = name
        self.fuel_price = price
        self.co2_emmision = emmision
        self.power_max = p_max
        self.power_min = p_min


class HydroPowerPlant():
    '''__tablename__ = "hydro"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    power_max = db.Column(db.Float, nullable=False)
    power_min = db.Column(db.Float, nullable=False)'''

    def __init__(self, id, name, p_min, p_max):
        self.id = id
        self.name = name
        self.hydro_power_max = p_max
        self.hydro_power_min = p_min


class WindPowerPlant():
    '''__tablename__ = "wind"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    ellise_lenght = db.Column(db.Float, nullable=False)
    ellise_parts = db.Column(db.Float, nullable=False)
    power_max = db.Column(db.Float, nullable=False)
    power_min = db.Column(db.Float, nullable=False)'''

    def __init__(self, id, name, ellise_lenght, p_min, p_max):
        self.id = id
        self.name = name
        self.ellise_lenght = ellise_lenght
        self.power_max = p_max
        self.power_min = p_min


class SolarPowerPlant():
    '''__tablename__ = "solar"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    surface_panel = db.Column(db.Float, nullable=False)
    panel_degree = db.Column(db.Float, nullable=False)
    power_max = db.Column(db.Float, nullable=False)
    power_min = db.Column(db.Float, nullable=False)'''

    def __init__(self, id, name, surface_panel, p_min, p_max):
        self.id = id
        self.name = name
        self.surface_panel = surface_panel
        self.power_max = p_max
        self.power_min = p_min