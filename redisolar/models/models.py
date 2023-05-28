from enum import Enum
from pydantic import BaseModel


class MetricUnit(Enum):
    """Supported measurement metrics"""

    WH_GENEREATED = "whG"
    WH_USED = "whU"
    TEMP_CELCIUS = "tempC"


class GeoUnit(Enum):
    """Geographic units available for geo queries."""

    M = "m"
    KM = "km"
    MI = "mi"
    FT = "ft"


class Coordinate(BaseModel):
    """A coordiante pair"""

    lng: float
    lat: float


class Site(BaseModel):
    """A solar power installation"""

    id: int
    capacity: float
    panels: int
    address: str
    city: str
    state: str
    postal_code: str
    coordinate: Coordinate | None = None
