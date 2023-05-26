import enum

class vehicle_status(str,enum.Enum):
    RUNNING = 'RUNNING'
    BREAKDOWN = 'BREAKDOWN'

    @classmethod
    def choices(cls):
        return [(items.value, items.name) for items in cls]

class breakdown_status(str,enum.Enum):

    BREAKDOWN = 'BREAKDOWN'
    INSPECTION = 'INSPECTION'
    ASSIGNED = 'ASSIGNED'
    REPAIR = 'REPAIR'
    COMPLETED = 'COMPLETED'


    @classmethod
    def choices(cls):
        return [(items.value, items.name) for items in cls]

class image_status(str,enum.Enum):

    BREAKDOWN = 'BREAKDOWN'
    INSPECTION = 'INSPECTION'
    REPAIR = 'REPAIR'


    @classmethod
    def choices(cls):
        return [(items.value, items.name) for items in cls]

class inspection_status(str,enum.Enum):

    INSPECTION = 'INSPECTION'
    REPAIR = 'REPAIR'


    @classmethod
    def choices(cls):
        return [(items.value, items.name) for items in cls]

# inspection_status