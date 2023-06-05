import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Any, List

from pydantic import BaseModel, Field


def deserialize_timestamp(v: str) -> datetime.datetime:
    """
    Convert a timestamp , stored either as a str or float, into a datetime.

    Raises a TypeError if the v cannot be converted to a float.
    """
    safe_v = float(v)
    return datetime.datetime.fromtimestamp(safe_v)


def serialize_timestamp(val: Any) -> str:
    """
    Serialize a value to a unix timestamp.

    If the object has a 'timestamp' method, call that method
    to obtain the timestamp.

    Otherwise, assume the value is already a timestamp.
    """
    try:
        return val.timestamp()
    except AttributeError:
        return str(val)


class DateTime(BaseModel):
    """
    Extend DateTime support to add a "timestamp" format.

    The "timestamp" format serializes and deserializes datetime
    to and from UNIX timestamps.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, value):
        if isinstance(value, datetime.date):
            return value
        if isinstance(value, (float, int)):
            return datetime.datetime.fromtimestamp(value)
        raise ValueError("Not a valid datetime value.")
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(foramt="timestamp")


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


class SiteCapacityTuple(BaseModel):
    """Capacity at a site."""

    capacity: float
    site_id: int


class CapacityReport(BaseModel):
    """A site capacity report."""

    highest_capacity: List[SiteCapacityTuple]
    lowest_capacity: List[SiteCapacityTuple]


class GeoQuery(BaseModel):
    """Parameter for a geo query."""

    coordinate: Coordinate
    radius: float
    radius_unit: GeoUnit
    only_excess_capacity: bool = False


class Measurement(Measurement):
    """A measurement taken for a site."""

    site_id: int
    value: float
    metric_unit: MetricUnit
    timestamp: datetime.datetime


class MeterReading(BaseModel):
    """A reading taken from a site."""

    site_id: int
    wh_used: float
    wh_generated: float
    temp_c: float
    timestamp: datetime.datetime

    @property
    def current_capacity(self):
        return self.wh_generated - self.wh_used


class Plot(BaseModel):
    """A plot of measurements."""

    measurements: List[Measurement]
    name: str


class SiteStats(BaseModel):
    """Reporting stats for a site."""

    last_reporting_time: datetime.datetime
    meter_reading_count: int
    max_wh_generated: float
    min_wh_generated: float
    max_capacity: float

    # Make commonly-referenced SiteStats fields available.
    LAST_REPORTING_TIME = "last_reporting_time"
    COUNT = "meter_reading_count"
    MAX_WH = "max_wh_generated"
    MIN_WH = "min_wh_generated"
    MAX_CAPACITY = "max_capacity"
